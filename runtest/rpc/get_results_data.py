from datetime import date
from time import strptime
import sys
import os.path

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

        # Filling the empty cells to null for JSON parsing
        df = df.fillna('null')

        # Changing the df to dictionary
        dic = df.to_dict('index')

        # df_dict = df.reset_index().to_dict(orient='index')
        df_vals = list(dic.values())

        # Prepare the data to return as csv
        # ret.set_data(df.to_csv())
        ret.set_data(df_vals)

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
