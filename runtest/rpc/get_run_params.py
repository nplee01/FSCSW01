from datetime import date
import sys
from django.http import JsonResponse

from runtest.models import ValueSet, ValueSetMember
from .return_record import ReturnRecord

def get_run_params(request):
    # Get Backtest Run parameters
    # handles get or post, we dont care
    ret = ReturnRecord()
    data = {}
    try:
        vs = ValueSet.objects.get(value_set_code='RUN-FIELDS')
        # Get Run Range
        rr = ValueSetMember.objects.get(value_set=vs, value_code='RUN-RANGE')
        # We store date as ordinal in Parameter
        data['start_date'] = date.fromordinal(rr.param_1.default_value)
        data['end_date'] = date.fromordinal(rr.param_2.default_value or 100000)
        # Get Portfolio Start amount
        pf = ValueSetMember.objects.get(value_set=vs, value_code='PORTFOLIO-START')
        data['portfolio_start'] = pf.param_1.default_value
        data['portfolio_start_min'] = pf.param_1.min_value
        data['portfolio_start_max'] = pf.param_1.max_value
        data['portfolio_start_step_by'] = pf.param_1.step_by 
        # Get Stop loss fields 
        sl = ValueSetMember.objects.get(value_set=vs, value_code='STOP-LOSS')
        data['stop_loss'] = sl.param_1.default_value
        data['stop_loss_min'] = sl.param_1.min_value
        data['stop_loss_max'] = sl.param_1.max_value
        data['stop_loss_step_by'] = sl.param_1.step_by
        # Version 0.1 does not need trailing stop loss
        # data['trail_stop_loss'] = sl.param_2.default_value
        ts = ValueSetMember.objects.get(value_set=vs, value_code='TRADE-SIZE')
        data['trade_size'] = ts.param_1.default_value
        data['trade_size_min'] = ts.param_1.min_value
        data['trade_size_max'] = ts.param_1.max_value
        data['trade_size_step_by'] = ts.param_1.step_by
        # Prepare data to be returned
        ret.set_data(data)
    # No exceptions expected if fixtures has been loaded
    except ValueSet.DoesNotExist as err:
        ret.set_error(str(err))
    except ValueSetMember.DoesNotExist as err:
        # We need line where error occured, many possible 
        (*_unused, tb) = sys.exc_info()
        ret.set_error(str(err) + ' @ line ' + str(tb.tb_lineno))
    except AttributeError as err:
        # In case some params not set
        (*_unused, tb) = sys.exc_info()
        ret.set_error(str(err) + ' @ line ' + str(tb.tb_lineno))
    # Return json
    return JsonResponse(ret.to_dict())

