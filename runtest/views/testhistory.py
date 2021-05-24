'''
1. Remark pop up dialog to add in remark
2. When Submit, do a POST call to the backend with the id of the record and remark field, update at the backend
3. Data table, add new RPC call for the data, submit the user id
4. Get user id, to get the data from the backtest
5. Can use a django form set in a template, just like the runtest which is using a form.

Require: User id then use a GET call from the backend to retrieve json data list

Generate some dummy data at the backend, select again the testrun table, 
Copy RPC anyone of those (getrunparam or getstartegy param), use the same ReturnRecord() to return the data
Add in the runtest/url.py, create a new rpc call
	1. import the function
	2. map the path to the function 
'''
from django.shortcuts import render
from django.http import HttpResponseRedirect

def testhistory(request):
    if request.user.is_authenticated:
        template_name= 'runtest/testhistory.html'
        # testhistorydata = history_set.historySet.objects.all()
        testhistorydata = test_run.objects.filter(run_by = request.user)
        return render(request, template_name, context={'testhistorydata': testhistorydata})
    else:
        return HttpResponseRedirect('accounts/login/?next=/testhistory')
    
