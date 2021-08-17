# Stock data maintenance 
import os
from datetime import date, datetime, timedelta

import yfinance as yf
import pandas as pd

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

# Get stock name from code
def get_stock_name(ticker):
    vs = ValueSet.objects.get(value_set_code='STOCKS')
    sm = ValueSetMember.objects.get(value_set=vs, value_code=ticker)
    return sm.value_description

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
def download_stock(ticker, start_date, end_date):
    # ticker as defined by yahoo finance, eg Tenaga is 5437.KL
    # Start and End dates for prices
    prices = yf.download(ticker, start=start_date, end=end_date, progress=False)
    stock_dir = get_stock_dir()
    stock_name = get_stock_name(ticker)
    csvf = os.path.join(stock_dir, stock_name + CSV)
    if os.path.exists(csvf):
        # Append to current csv file
        prices.to_csv(csvf, mode='a', header=False)
    else:
        # New file
        prices.to_csv(csvf)
    # Rows downloaded
    return len(prices)

# Download all stocks based on our ValueSet(STOCKS) and last download date
# Added to runtest/management/commands as stockdata. You may run this as
# './manage.py stockdata'
def download_all_stocks(end_date=None):
    vs = ValueSet.objects.get(value_set_code='STOCKS')
    (start_date, last_download_date) = get_last_download_date()
    if last_download_date:
        # Incremental download from last download date + 1
        start_date = last_download_date + timedelta(days=1)
    # else is the initial fixtures RUN-START
    
    if end_date is None:
        # Set end download date to either today or yesterday
        if datetime.now().hour > 20:
            # End of Day process after 8 pm
            end_date = date.today()
        else:
            end_date = date.today() + timedelta(days=-1)
    
    # Skip if last download = end date
    if last_download_date == end_date:
        print(f"Last download is already up to date as at {last_download_date}")
        return

    print(f"Downloading from {start_date} to {end_date}....")
    for stock in [st.value_code for st in ValueSetMember.objects.filter(value_set=vs)]:
        rows = download_stock(stock, start_date, end_date)
        print(f"{stock}: Downloaded {rows} rows")
    # Update last download date
    update_last_download(end_date)

# Read all stock prices and prepare as dataframe. 
def read_stock(stock_name, start_date, end_date):
    stock_dir = get_stock_dir()
    df = pd.read_csv(os.path.join(stock_dir, stock_name + CSV), parse_dates = ["Date"])
    datetime_series = pd.to_datetime(df['Date'])
    datetime_index = pd.DatetimeIndex(datetime_series.values)
    df = df.set_index(datetime_index)
    return df.loc[start_date.isoformat() : end_date.isoformat()]
