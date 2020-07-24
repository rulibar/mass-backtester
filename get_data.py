"""
get_data.py
"""

from datetime import datetime, timezone
from binance.client import Client

# user vars
api_key = ""
api_secret = ""
client = Client(api_key, api_secret)

n_early_candles = 600 # Number of early candles for indicators

pair = 'BNBBTC' # Ex: 'BNBBTC'
interval_mins = 120 # Ex: 5, 15, 30, 60, 120, 240, 360, 480, 720, 1440

start_year = 2020 # Ex: 2020
start_month = 1 # Ex: 1 to 12
start_day = 1 # Ex: 1 to 31

end_year = 2020
end_month = 2
end_day = 1

# main code
if interval_mins in {5, 15, 30}: interval = "{:.0f}m".format(interval_mins)
elif interval_mins in {60, 120, 240, 360, 480, 720}: interval = "{:.0f}h".format(interval_mins / 60)
elif interval_mins in {1440}: interval = "{:.0f}d".format(interval_mins / 60 / 24)
else: exit()

start_date = datetime(start_year, start_month, start_day, tzinfo=timezone.utc)
start_date = start_date.timestamp()
start_date_adj = start_date - 60 * interval_mins * (n_early_candles + 10)
start_date = int(1000 * start_date)
start_date_adj = int(1000 * start_date_adj)
end_date = datetime(end_year, end_month, end_day, tzinfo=timezone.utc)
end_date = int(1000 * end_date.timestamp())
candles = client.get_historical_klines(pair, interval, start_date_adj, end_date)

extra_candles = 0
for candle in candles:
    if start_date > candle[0]: extra_candles += 1
    else: break
excess = extra_candles - n_early_candles
candles = candles[excess:]
