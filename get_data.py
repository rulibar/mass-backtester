"""
get_data.py v1.0.3 (20-11-07)
https://github.com/rulibar/mass-backtester
Gets historical candle data from Binance for a specified pair, interval, start
date, and end date. Gets a specified number of early candles for calculating
indicators.

Output:
btc_eth_120m_200101-200301.txt
[
    1573502400000,      // Open time
    '0.02128900',       // Open
    '0.02130100',       // High
    '0.02126800',       // Low
    '0.02130000',       // Close
    '3221.45600000',    // Volume
    1573509599999,      // Close time
    '68.56577333',      // Quote asset volume
    5295,               // Number of trades
    '1564.35900000',    // Taker buy base asset volume
    '33.29836240',      // Taker buy quote asset volume
    '0'                 // Ignore
]
Format of data directly from Binance API.
The first entry in the data is the oldest.

v1.0.1 (20-7-30)
- Take asset/base instead of pair
- Change the naming scheme of data files
    - Use currency pair instead of pair (BTC_ETH instead of ETHBTC)
    - Use interval_mins instead of interval (120m instead of 2h)

v1.0.2 (20-8-29)
- Say how many lines of data were saved

v1.0.3 (20-11-07)
- Stop putting 0's in front of the month or day if it equals 10
    - Use >= sign when creating the file name

"""

from datetime import datetime, timezone
from binance.client import Client

# user vars
api_key = ""
api_secret = ""
client = Client(api_key, api_secret)

n_early_candles = 600 # Number of early candles for indicators

asset = 'ETH' # Ex: 'ETH'
base = 'BTC' # Ex: 'BTC'
interval_mins = 120 # Ex: 5, 15, 30, 60, 120, 240, 360, 480, 720, 1440

start_year = 2020 # Ex: 2020
start_month = 1 # Ex: 1 to 12
start_day = 1 # Ex: 1 to 31

end_year = 2020
end_month = 2
end_day = 1

# set interval
if interval_mins in {5, 15, 30}: interval = "{:.0f}m".format(interval_mins)
elif interval_mins in {60, 120, 240, 360, 480, 720}: interval = "{:.0f}h".format(interval_mins / 60)
elif interval_mins in {1440}: interval = "{:.0f}d".format(interval_mins / 60 / 24)
else: exit()

# set dates
start_date = datetime(start_year, start_month, start_day, tzinfo=timezone.utc)
start_date = start_date.timestamp()
start_date_adj = start_date - 60 * interval_mins * (n_early_candles + 10)
start_date = int(1000 * start_date)
start_date_adj = int(1000 * start_date_adj)
end_date = datetime(end_year, end_month, end_day, tzinfo=timezone.utc)
end_date = int(1000 * end_date.timestamp())

# main code
pair = "{}{}".format(asset, base)
currency_pair = "{}_{}".format(base, asset)
candles = client.get_historical_klines(pair, interval, start_date_adj, end_date)

early_candles = 0
for candle in candles:
    if candle[0] < start_date: early_candles += 1
    else: break
excess = early_candles - n_early_candles
candles = candles[excess:]

candles_str = str()
num_lines = 0
for candle in candles:
    candles_str += str(candle) + "\n"
    num_lines += 1

file_name = currency_pair.lower()
file_name += "_" + str(interval_mins) + "m"
file_name += "_" + str(start_year)[-2:]
if start_month >= 10: file_name += str(start_month)
else: file_name += "0" + str(start_month)
if start_day >= 10: file_name += str(start_day)
else: file_name += "0" + str(start_day)
file_name += "-" + str(end_year)[-2:]
if end_month >= 10: file_name += str(end_month)
else: file_name += "0" + str(end_month)
if end_day >= 10: file_name += str(end_day)
else: file_name += "0" + str(end_day)
file_name += ".txt"

with open(file_name, "w") as f: f.write(candles_str)

print("Successfully saved {} lines of data to {}.".format(num_lines, file_name))
