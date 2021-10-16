from datetime import date
from time import strptime
import sys
import os.path
import simplejson

import pandas as pd

from django.http import JsonResponse
from django.conf import settings

from runtest.models import TestRun
from .return_record import ReturnRecord


def get_results_data(request, run_id):
    # Get results data

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
        df = pd.read_excel(os.path.join(
            settings.RESULTS_DIR, str(run_id) + 'G.xlsx'))

        # TODO: Drop the first unnamed column
        df = df.iloc[:, 1:]

        # TODO: Change the date format
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

        # Getting the list of dict for the json
        df_vals = list(df.T.to_dict().values())

        # Prepare the data to return as json obj
        ret.set_data(simplejson.loads(simplejson.dumps(df_vals, ignore_nan=True)))

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
