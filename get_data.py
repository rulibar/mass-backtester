"""
"""

from datetime import datetime, timezone
from binance.client import Client

# user vars
api_key = ""
api_secret = ""
client = Client(api_key, api_secret)

pair = 'BNBBTC' # Ex: 'BNBBTC'
interval = '30m' # Ex: '30m', '2h', '1d'

start_year = 2020 # Ex: 2020
start_month = 1 # Ex: 1 to 12
start_day = 1 # Ex: 1 to 31

end_year = 2020
end_month = 2
end_day = 1

# main code
start_date = datetime(start_year, start_month, start_day, tzinfo=timezone.utc)
start_date = int(1000 * start_date.timestamp())
end_date = datetime(end_year, end_month, end_day, tzinfo=timezone.utc)
end_date = int(1000 * end_date.timestamp())
candles = client.get_historical_klines(pair, interval, start_date, end_date)

for candle in candles: print(candle)
print(len(candles))
