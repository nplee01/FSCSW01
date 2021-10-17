from runtest.views.graphsummary import graphsummary
from django.shortcuts import render
from django.utils import timezone

from runtest.forms.test_run import TestRunForm
from runtest.models import TestRun, ValueSet, ValueSetMember
from runtest.stocks import get_stock
from btengine.api import api_bt_run

import os
import json
from datetime import datetime
from django.conf import settings


def get_strategy_desc(strategy, indicators):
    vs = ValueSet.objects.get(value_set_code='STRATEGIES')
    stg = ValueSetMember.objects.get(value_set=vs, value_code=strategy)
    desc = stg.value_description
    vs = ValueSet.objects.get(value_set_code='INDICATORS')
    for ind in indicators:
        vsm = ValueSetMember.objects.get(value_set=vs, value_code=ind[0])
        desc += vsm.value_description
    return desc


def backtest(request):
    """
    Allow user to select input parameters for a back test and
    subsequently run the back test when form is submitted
    """
    template_name = 'runtest/backtest.html'

    if request.method == 'POST':
        if request.user.is_authenticated:
            usr = request.user
        else:
            usr = None

        obj = TestRun(run_by=usr, run_status='EXE', run_on=timezone.now(),
                      exec_start_on=timezone.now())
        # Handle submitted form
        form = TestRunForm(instance=obj, data=request.POST)
        # Validate the form
        if form.is_valid():
            form.save()
            # Prepare to call
            ticker = form.cleaned_data.get('stock_ticker')
            stock = get_stock(ticker)
            indicators = []
            for i in range(1, 3):
                ind = form.cleaned_data.get('indicator_' + str(i) + '_code')
                if ind:
                    params = [ind]
                    for j in range(1, 6):
                        param = form.cleaned_data.get(
                            'ind_' + str(i) + '_param_' + str(j))
                        if param:
                            params.append(param)
                    indicators.append(params)

            # Indicators looks like [['SMA', 10, 20], ['XMA', 100, 200, 300]]
            desc = get_strategy_desc(
                form.cleaned_data['strategy_code'], indicators)

            # Indicators used to be display on the test history page
            # FIXME: TEMP FIX BEFORE FOUND HOW TO RESET THE DEFAULT VALUES
            # FROM THE BACKTEST FORM
            indicators_str = ''
            for ind in indicators:
                indicators_str += f'{ind[0]} ' + str([i for i in ind[1:]]) + ', '

            # Remove the last ', '
            indicators_str = indicators_str[:-2]

            # Replacing the [ ] to ( )
            indicators_str = indicators_str.replace('[', '(').replace(']', ')')

            # Change the XMA to SMA Crossing (To be converted into a functions
            # if there are many indicators)
            indicators_str = indicators_str.replace('XMA', 'SMA Crossing')

            # Call backtest
            status = api_bt_run(form.instance.id, stock.value_description, form.cleaned_data['start_date'],
                                form.cleaned_data['end_date'], form.cleaned_data['portfolio_start'],
                                form.cleaned_data['trade_size'], desc, form.cleaned_data['strategy_code'], indicators)

            # Update the database using the excel
            sm = json.load(
                open(os.path.join(settings.RESULTS_DIR, str(form.instance.id) + 'P.json')))

            # Add the data into the database
            form.instance.stock_ticker = stock.value_description
            form.instance.portfolio_end = sm['FinalEquity']
            form.instance.equity_performance = sm['FinalEquity']
            form.instance.equity_roi = sm['EquityROI']
            form.instance.trades = sm['TradeCount']
            form.instance.win_trades = sm['ProfitTradeCount']
            form.instance.lose_trades = sm['LossingTradeCount']
            form.instance.win_rate = sm.get('WinRate', '0')
            form.instance.max_drawdown = sm.get('MaxDrawdownValue', '0')
            form.instance.indicators = indicators_str

            # FIXME: 0 cannot be render on graphing.html

            try:
                max_drawdown_date = datetime.strptime(
                    sm['MaxDrawdownDate'], '%d-%m-%Y')
                form.instance.drawdown_date = f'{max_drawdown_date:%Y-%m-%d}'
            except:
                form.instance.drawdown_date = form.cleaned_data['end_date']

            # TODO: !!! CHECKING NEEDED !!!
            # form.instance.avg_win_amount = sm['WinRate'] / \
            #     100 * sm['InitCapital']
            # form.instance.avg_loss_amount = (
            #     (100 - sm['WinRate'])/100) * sm['InitCapital']

            # Update as completed
            form.instance.exec_end_on = timezone.now()
            form.instance.run_status = 'COM'
            form.instance.save()

            return graphsummary(request, form.instance.id)
    else:
        # New form
        form = TestRunForm()
    return render(request, template_name, context={'form': form})
