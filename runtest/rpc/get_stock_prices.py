from datetime import date
from time import strptime
import sys
from django.http import JsonResponse

from runtest.models import ValueSet, ValueSetMember
from .return_record import ReturnRecord
from runtest.utils import to_date
from btengine.stocks import read_stock

def get_stock_prices(request, stock_name, start_date, end_date):
    # Get stock prices for a stock by name and date range
    # Dates are iso format as string

    # handles get only
    ret = ReturnRecord()
    # Extract the parameters passed in
    if request.method == 'GET':
        params = request.GET
    else:
        raise Exception('Only Get request accepted')

    try:
        p_start_date = to_date(start_date) 
        p_end_date = to_date(end_date) 
    except ValueError:
        raise Exception('Invalid start or end date')

    try:
        vs = ValueSet.objects.get(value_set_code='STOCKS')
        rr = ValueSetMember.objects.get(value_set=vs, value_description=stock_name)
        # We store date as ordinal in Parameter
        rr_start = date.fromordinal(rr.param_1.default_value)
        rr_end = date.fromordinal(rr.param_2.default_value)
        # Validate that the start/end requested within range
        if p_start_date < rr_start or p_end_date > rr_end:
            raise Exception(f'Start or End date beyond our available range of {rr_start} to {rr_end}')
        # Get the data as a pandas dataframe
        df = read_stock(stock_name, p_start_date, p_end_date)
        # Prepare the data to return as csv
        ret.set_data(df.to_csv())
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
    except Exception as err:
        ret.set_error(str(err))
    # Return json
    return JsonResponse(ret.to_dict())

