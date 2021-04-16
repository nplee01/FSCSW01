from django.shortcuts import render

def dispatcher(request, template_name):        
    """
    Dispatch a template. To be used in urls.py
    for static templates.

    eg
        path('home', dispatcher, {'template_name': 'runtest/home.html'}, name='home'),
    """
    return render(request, template_name)
