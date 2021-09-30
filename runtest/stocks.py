# Stock data maintenance 
import os
from datetime import date, datetime, timedelta

import yfinance as yf

from django.conf import settings

from runtest.models import ValueSet, ValueSetMember

CSV = '.csv'

# Get the directory to store stock prices
def get_stock_dir():
    stock_dir = settings.STOCK_DIR
    # Create the directory if it does not exist
    if not os.path.exists(stock_dir):
        os.mkdir(stock_dir)
        os.chmod(stock_dir, 0o775)
    return stock_dir

# Get last download's start/end date
def get_run_range():
    vs = ValueSet.objects.get(value_set_code='RUN-FIELDS')
    # Get Run Range
    return ValueSetMember.objects.get(value_set=vs, value_code='RUN-RANGE')

# Get stock 
def get_stock(ticker):
    vs = ValueSet.objects.get(value_set_code='STOCKS')
    sm = ValueSetMember.objects.get(value_set=vs, value_code=ticker)
    return sm

def get_last_download_date():
    rr = get_run_range()
    # We store date as ordinal in Parameter
    # Param 1 = start date, Param 2 = Last download date (initially None)
    start_date = date.fromordinal(rr.param_1.default_value) if isinstance(rr.param_1.default_value, int) else None
    end_date = date.fromordinal(rr.param_2.default_value) if isinstance(rr.param_2.default_value, int) else None
    return (start_date, end_date)

def update_last_download(download_date):
    rr = get_run_range()
    # We change the End Date only
    rr.param_2.default_value = download_date.toordinal()
    rr.param_2.save()

# Download a single stock prices
def download_stock(ticker, start_date, end_date, first_download):
    # ticker as defined by yahoo finance, eg Tenaga is 5437.KL
    # Start and End dates for prices
    stock = get_stock(ticker)
    stock_name = stock.value_description
    # Override start date if later than stock's last price date
    if stock.param_2.default_value:
        last_download = date.fromordinal(stock.param_2.default_value)
        if start_date > last_download:
            start_date = last_download + timedelta(days=1)
    # Assert start >= end
    if end_date < start_date:
        print(f"Stock {stock_name}: Start {start_date} must be earlier or same as End {end_date}")
        return 0
    # Start download from yahoo
    prices = yf.download(ticker, start=start_date, end=end_date, progress=False)
    stock_dir = get_stock_dir()
    csvf = os.path.join(stock_dir, stock_name + CSV)
    # Save to file
    if os.path.exists(csvf):
        # Append to current csv file
        prices.to_csv(csvf, mode='a', header=False)
    else:
        # New file
        prices.to_csv(csvf)
    # Update download dates to stocks
    # Note: Some stocks may not have prices up to end date,
    # so last_date <= end_date
    last_date = prices.index[-1] # Last Row
    if first_download:
        # Get earliest date from prices downloaded
        first_date = prices.index[0] # First Row
        stock.param_1.default_value = first_date.toordinal()
        stock.param_1.save()
    stock.param_2.default_value = last_date.toordinal()
    stock.param_2.save()
    # Rows downloaded
    return len(prices)

# Download all stocks based on our ValueSet(STOCKS) and last download date
# Added to runtest/management/commands as stockdata. You may run this as
# './manage.py stockdata'. You should schedule this as a cron job with 
# command "cd home_dir; ./manage.py stockdata"
def download_all_stocks(end_date=None):
    (start_date, last_download_date) = get_last_download_date()
    if last_download_date:
        # Incremental download from last download date + 1
        start_date = last_download_date + timedelta(days=1)
        first_download = False
    else:
        # else is the initial fixtures RUN-START
        # Need to update start date for stocks
        first_download = True
    
    # Yahoo data is at least 1 day behind. Safer to schedule this every Sunday night
    if datetime.now().hour > 20:
        # End of Day process after 8 pm
        last_date = date.today() + timedelta(days=-1)
    else:
        last_date = date.today() + timedelta(days=-2)
    if end_date is None:
        end_date = last_date
    # Skip if request end date not available
    if end_date > last_date:
        print(f"Latest price date available is {last_date}")
        return
    # Skip if last download = end date
    if last_download_date == end_date:
        print(f"Last download is already up to date as at {last_download_date}")
        return
    # Assert start >= end
    if end_date < start_date:
        print(f"Start {start_date} must be earlier or same as End {end_date}")
        return

    print(f"Downloading from {start_date} to {end_date}....")
    vs = ValueSet.objects.get(value_set_code='STOCKS')
    for stock, stock_name in [(st.value_code, st.value_description) 
            for st in ValueSetMember.objects.filter(value_set=vs)]:
        rows = download_stock(stock, start_date, end_date, first_download)
        print(f"{stock_name}: Downloaded {rows} rows")
    # Update last download date
    update_last_download(end_date)
