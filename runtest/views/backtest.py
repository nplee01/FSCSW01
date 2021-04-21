from django.shortcuts import render

from runtest.forms.test_run import TestRunForm

def backtest(request):        
    """
    Allow user to select input parameters for a back test and
    subsequently run the back test when form is submitted
    """
    template_name = 'runtest/backtest.html'

    # Get request
    form = TestRunForm()
    return render(request, template_name, context={'form': form})
