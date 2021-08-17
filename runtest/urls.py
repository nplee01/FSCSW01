# runtest URL Configuration
from django.urls import path, re_path

# RPC Calls
from runtest.rpc.get_run_params import get_run_params
from runtest.rpc.get_strategy_params import get_strategy_params
from runtest.rpc.get_indicator_params import get_indicator_params
from runtest.rpc.get_sizing_params import get_sizing_params
from runtest.rpc.get_stock_prices import get_stock_prices
# from runtest.rpc.get_test_history import get_test_history

urlpatterns = [
        path('rpc/GetRunParams', get_run_params),
        re_path('rpc/GetStrategyParams/(?P<strategy_code>[A-Z0-9\-]+)', get_strategy_params),
        re_path('rpc/GetIndicatorParams/(?P<indicator_code>[A-Z0-9\-]+)', get_indicator_params),
        re_path('rpc/GetSizingParams/(?P<sizing_code>[A-Z0-9\-]+)', get_sizing_params),
        re_path('rpc/GetStockPrices/(?P<stock_name>[A-Z0-9\-\.]+)/(?P<start_date>\d{4}\-\d{2}\-\d{2})/(?P<end_date>\d{4}\-\d{2}\-\d{2})', get_stock_prices),
]
