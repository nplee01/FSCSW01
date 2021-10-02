import json
import requests
from django.shortcuts import render


def graphsummary(request, run_id):

    # call rpc for summary
    summary = requests.get(
        f"http://localhost:8000/runtest/rpc/GetResultsSummary/{run_id}")

    summary_json = json.loads(summary.text)

    return render(request, 'runtest/graphing3.html', {'summary': summary_json['data'], 'run_id': run_id})

# {'StockName': 'TENAGA', 'InitCapital': 10000, 'FinalEquity': 18229.999542236335,
# 'CurrentShareMarketValue': 0.0, 'CurrentCashBalance': 18229.999542236335,
# 'EquityPerfomance': 8229.999542236335, 'EquityROI': 82.29999542236335,
# 'TradeCount': 15, 'ProfitTradeCount': 9, 'LossingTradeCount': 6,
# 'WinRate': 60.0, 'MaxDrawdownValue': 1830.0008773803638,
# 'MaxDrawdownDate': '03-06-2021'}
