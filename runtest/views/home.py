from django.shortcuts import render

def home(request):        
    """
    Home Page
    """
    return render(request, 'runtest/home.html')
