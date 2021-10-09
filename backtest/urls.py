"""backtest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from runtest.views import dispatcher, backtest, testhistory, graphsummary

urlpatterns = [
    # We are using 3rd party allauth app for authentication
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('', dispatcher, {'template_name': 'runtest/home.html'}, name='home'),  
    path('backtest', backtest, name='backtest'),  
    path('howitworks', dispatcher, {'template_name': 'runtest/howitworks.html'}, name='howitworks'),
    path('testhistory', testhistory, name='testhistory'),
    path('testhistory/update', testhistory, name='testhistoryupdate'),
    path('testhistory/<int:id>/delete/', testhistory, name='testhistorydelete'),
    path('about', dispatcher, {'template_name': 'runtest/about.html'}, name='about'),  
    path('graphing', dispatcher, {'template_name': 'runtest/graphing.html'}, name='graphing'),  
    path('graphing2', dispatcher, {'template_name': 'runtest/graphing2.html'}, name='graphing'),  
    path('graphing3/<int:run_id>/', graphsummary, name='summary'),  
    path('runtest/', include('runtest.urls')),
]
