# mass-backtester
A program to test a binance-pybot strategy on multiple sets of historical price data.

### How it works
- create a folder called data/
- use get_data.py to fill the data folder with sets of price data
- update init and strat methods in maba.py to the strategy of your choosing
- setup the output to summary.txt at the end of maba.py
- run maba.py
- it tests the strategy on all of the sets of price data and saves the results to summary.txt
