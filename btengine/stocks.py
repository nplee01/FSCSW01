# Stock data maintenance 
import os.path
from pathlib import Path
import pandas as pd

# Must match what is defined in django.settings.STOCK_DIR
# If we use django settings, then cannot run this as a script!
STOCK_DIR = Path(__file__).resolve().parent.parent / 'stockdata'

# Read all stock prices and prepare as dataframe. 
def read_stock(stock_name, start_date, end_date):

    df = pd.read_csv(os.path.join(STOCK_DIR, stock_name + '.csv'), parse_dates = ["Date"])
    datetime_series = pd.to_datetime(df['Date'])
    datetime_index = pd.DatetimeIndex(datetime_series.values)
    df = df.set_index(datetime_index)
    return df.loc[start_date.isoformat() : end_date.isoformat()]
