# runtest URL Configuration
from django.urls import path, re_path

# RPC Calls
from runtest.rpc.get_run_params import get_run_params
from runtest.rpc.get_strategy_params import get_strategy_params
from runtest.rpc.get_indicator_params import get_indicator_params

urlpatterns = [
        path('rpc/GetRunParams', get_run_params),
        re_path('rpc/GetStrategyParams/(?P<strategy_code>[A-Z0-9\-]+)', get_strategy_params),
        re_path('rpc/GetIndicatorParams/(?P<indicator_code>[A-Z0-9\-]+)', get_indicator_params),
]
