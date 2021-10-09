import json
import requests
from django.shortcuts import render
from runtest.models.test_run import TestRun

# Default: GET
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

def graphsummary(request, run_id):

    # call rpc for summary
    summary = requests.get(
        f"http://localhost:8000/runtest/rpc/GetResultsSummary/{run_id}")

    summary_json = json.loads(summary.text)
    
    # TODO: If else condition
    testhistorydata = TestRun.objects.filter(run_by = request.user)
    
    tmpRemark = TestRun.objects.get(id = run_id).user_remarks

    remark = "" if tmpRemark == None else tmpRemark

    return render(request, 'runtest/graphing3.html', {'summary': summary_json['data'], 'run_id': run_id, 'remark': remark})

# {'StockName': 'TENAGA', 'InitCapital': 10000, 'FinalEquity': 18229.999542236335,
# 'CurrentShareMarketValue': 0.0, 'CurrentCashBalance': 18229.999542236335,
# 'EquityPerfomance': 8229.999542236335, 'EquityROI': 82.29999542236335,
# 'TradeCount': 15, 'ProfitTradeCount': 9, 'LossingTradeCount': 6,
# 'WinRate': 60.0, 'MaxDrawdownValue': 1830.0008773803638,
# 'MaxDrawdownDate': '03-06-2021'}


@csrf_protect
@login_required
def update(request, id=None, remark=None):
    
    if request.method == "POST":
        if remark and id != None:
            row = TestRun.objects.get(id = id)
            row.user_remarks = remark
        
    template_name = 'runtest/home.html'
    return render(request, template_name)


@login_required
@csrf_protect
def delete_entry(request):

    # Get the id and delete
    if request.method == "DELETE":
        if id in TestRun:
            row = TestRun.objects.get(id = id)
            print(row)
            
            # To check if the current id is runby the current user 
            # before deleting
            if request.user in row['run_by']:
                print('deleted')
                # TestRun.objects.filter(id = id).delete()

    template_name= 'runtest/testhistory.html'
    testhistorydata = TestRun.objects.filter(run_by = request.user)
    return render(request, template_name, context={'testhistorydata': testhistorydata})
