from datetime import date
from time import strptime
import sys, os.path, json

from django.http import JsonResponse
from django.conf import settings

from runtest.models import TestRun
from .return_record import ReturnRecord

def get_results_summary(request, run_id):
    # Get results summary

    # handles get only
    ret = ReturnRecord()
    # Extract the parameters passed in
    if request.method == 'GET':
        params = request.GET
    else:
        raise Exception('Only Get request accepted')

    try:
        testrun = TestRun.objects.get(pk=run_id)
        # Get the excel file
        sm = json.load(open(os.path.join(settings.RESULTS_DIR, str(run_id) + 'P.json')))
        # Prepare the data to return as csv
        ret.set_data(sm)
    # No exceptions expected if fixtures has been loaded
    except TestRun.DoesNotExist as err:
        ret.set_error(str(err))
    except AttributeError as err:
        # In case some params not set
        (*_unused, tb) = sys.exc_info()
        ret.set_error(str(err) + ' @ line ' + str(tb.tb_lineno))
    except Exception as err:
        ret.set_error(str(err))
    # Return json
    return JsonResponse(ret.to_dict())

