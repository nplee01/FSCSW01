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
import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect

from runtest.models import TestRun

# Default: GET
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect


@login_required
@csrf_protect
def testhistory(request, id=None):
    # This will handle Get, Post and Delete requests. I have changed urls.py to call this
    # view and your 2 functions below is not used.
    # id passed in only for Delete

    # CSRF Protect means that all non-GET methods needs to supply a Header X-CSRFToken 
    # with the cookie(csrftoken) that django sends with the original Get request.
    template_name= 'runtest/testhistory.html'

    if request.method == 'POST':
        # Handle the update request
        id = request.POST.get('id')
        rmk = request.POST.get('remarks')
        # Perform the update
        if id:
            row = TestRun.objects.get(pk=id)
            row.user_remarks = rmk
            row.save()
    elif request.method == 'DELETE':
        if id:
            row = TestRun.objects.get(pk=id)
            row.delete()

            # Delete the files
            orders_filepath = os.path.join(settings.RESULTS_DIR, str(id) + 'G.xlsx')
            performance_filepath = os.path.join(settings.RESULTS_DIR, str(id) + 'P.json')
            try:
                os.remove(orders_filepath)
                os.remove(performance_filepath)
            except:
                pass

    # Handle Get here or fallthru from handling Post and Delete to requery and redisplay data
    testhistorydata = TestRun.objects.filter(run_by = request.user)
    return render(request, template_name, context={'testhistorydata': testhistorydata})


# https://stackoverflow.com/questions/29212713/update-django-database-through-javascript
# https://www.geeksforgeeks.org/update-view-function-based-views-django/
# https://docs.djangoproject.com/en/3.2/topics/http/urls/
# @csrf_protect
# @login_required
# def update(request, id=None, remark=None):
    
#     if request.method == "POST":
#         if remark and id != None:
#             row = TestRun.objects.get(id = id)
#             row.user_remarks = remark
        
#     template_name = 'runtest/home.html'
#     return render(request, template_name)


# @login_required
# @csrf_protect
# def delete_entry(request):

#     # Get the id and delete
#     if request.method == "DELETE":
#         if id in TestRun:
#             row = TestRun.objects.get(id = id)
#             print(row)
            
#             # To check if the current id is runby the current user 
#             # before deleting
#             if request.user in row['run_by']:
#                 print('deleted')
#                 # TestRun.objects.filter(id = id).delete()

#     template_name= 'runtest/testhistory.html'
#     testhistorydata = TestRun.objects.filter(run_by = request.user)
#     return render(request, template_name, context={'testhistorydata': testhistorydata})
