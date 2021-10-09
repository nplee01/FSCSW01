import json
import requests
import sys
import os.path
import json
from django.shortcuts import render
from runtest.models.test_run import TestRun

# Default: GET
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect


def graphsummary(request, run_id):

    # call rpc for summary
    summary = requests.get(
        f"http://localhost:8000/runtest/rpc/GetResultsSummary/{run_id}")

    # Data to be rendered
    summary_json = json.loads(summary.text)

    if str(request.user) == 'AnonymousUser':
        # Render visitor page
        return render(request, 'runtest/visitorgraphing.html', {'summary': summary_json['data'], 'run_id': run_id, 'remark': ""})

    # For the user
    # Remark from the user
    tmpRemark = TestRun.objects.get(id=run_id).user_remarks
    # To avoid "None" in the summary page text area
    remark = "" if tmpRemark == None else tmpRemark

    return render(request, 'runtest/graphing3.html', {'summary': summary_json['data'], 'run_id': run_id, 'remark': remark})

# {'StockName': 'TENAGA', 'InitCapital': 10000, 'FinalEquity': 18229.999542236335,
# 'CurrentShareMarketValue': 0.0, 'CurrentCashBalance': 18229.999542236335,
# 'EquityPerfomance': 8229.999542236335, 'EquityROI': 82.29999542236335,
# 'TradeCount': 15, 'ProfitTradeCount': 9, 'LossingTradeCount': 6,
# 'WinRate': 60.0, 'MaxDrawdownValue': 1830.0008773803638,
# 'MaxDrawdownDate': '03-06-2021'}
