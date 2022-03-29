# https://backtest-rookies.com/2017/08/22/backtrader-multiple-data-feeds-indicators/

from datetime import datetime, timedelta 
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas_ta as ta
import backtrader as bt

from strategy_01 import *

# Extract a bunch of historical data return a multi-index dataframe
def get_prices_for(yahoo_symbol, start_date="2019-01-01", end_date=None): 
  #end_date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
  
  if end_date is None:
    end_date = str(datetime.now().strftime("%Y-%m-%d"))
    
  #yahoo_symbol = tsx_list[2]
  #data = yf.download(yahoo_symbol,start=start_date, end=end_date, progress=False)
  data = yf.download(tickers=yahoo_symbol,start=start_date, end=end_date, progress=True, group_by='ticker')
  if len(data) > 0:
    return data
  else:
    return None



if __name__ == "__main__":
  ### PREDEFINED DATASETS ###
  
  # Innovation fund companies listed
  ARKK_fund = pd.read_csv("https://raw.githubusercontent.com/poivronjaune/stock_screener/main/DATASETS/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv")
  ARKK_fund.rename(columns={'ticker':'Symbol'}, inplace=True)
  ARKK_fund = ARKK_fund.dropna()
  
  # ARKK_fund["Symbol"].to_list()
  # Symbols lists
  nasdaq_companies = pd.read_csv("https://raw.githubusercontent.com/poivronjaune/stock_screener/main/DATASETS/NASDAQ.csv")
  no_sector        = nasdaq_companies.loc[nasdaq_companies['Sector'].isna()].copy()
  basic_industries = nasdaq_companies.loc[nasdaq_companies['Sector'] == "Basic Industries"].copy()
  capital_goods    = nasdaq_companies.loc[nasdaq_companies['Sector'] == "Capital Goods"].copy()
  consumer_durable = nasdaq_companies.loc[nasdaq_companies['Sector'] == "Consumer Durables"].copy()
  consumer_non_dur = nasdaq_companies.loc[nasdaq_companies['Sector'] == "Consumer Non-Durables"].copy()
  consumer_services= nasdaq_companies.loc[nasdaq_companies['Sector'] == "Consumer Services"].copy()
  energy           = nasdaq_companies.loc[nasdaq_companies['Sector'] == "Energy"].copy()
  finance          = nasdaq_companies.loc[nasdaq_companies['Sector'] == "Finance"].copy()
  health_care      = nasdaq_companies.loc[nasdaq_companies['Sector'] == "Health Care"].copy()
  miscellaneous    = nasdaq_companies.loc[nasdaq_companies['Sector'] == "Miscellaneous"].copy()
  public_utilities = nasdaq_companies.loc[nasdaq_companies['Sector'] == "Public Utilities"].copy()
  technology       = nasdaq_companies.loc[nasdaq_companies['Sector'] == "Technology"].copy()
  transportation   = nasdaq_companies.loc[nasdaq_companies['Sector'] == "Transportation"].copy()
  
  
  ### ADJUST THIS SECTION TO USE YOUR SYMBOLS LIST ###
  #companies = ['ORCL','ZM', 'MSFT', 'AAPL', 'GATEU'] # For testing purposes
  companies = ['ORCL', 'AAPL', 'GATEU']
  #companies = ARKK_fund["Symbol"].to_list()
  #companies = transportation["Symbol"].to_list()
  
  
  
  print(f"Fetching price data for {len(companies)} symbols")
  start_of_price_data   = "2018-01-01"                                                            # Historical data start_date
  end_of_price_data     = datetime.today().strftime('%Y-%m-%d')                                   # Historical data end_date
  apply_strategy_on     = "2021-10-01"                                                            # Strategy apply date (skip price data before this date)
  minimum_data_required = 300                                                                     # Minimum price data that must be fetched for strategy to work
                                                                                                  # Strategy will apply to least number of data (example ORCL has 300 days, GATEU has 30 days)
  
  prices = get_prices_for(companies, start_date=start_of_price_data, end_date=end_of_price_data)
  
  # SETUP Backtrader portfolio info and commisions
  cash = 3000
  cerebro = bt.Cerebro()
  cerebro.broker.set_cash(cash)
  cerebro.broker.setcommission(commission=0.001)
  print('\n\nStarting Portfolio Value: %.2f' % cerebro.broker.getvalue())
  
  # SETUP a strategy to run on our data
  cerebro.addstrategy(strategy_RB, apply_date=apply_strategy_on, risk_to_reward=1.53, hold=20, log_to_screen=True)
  # Buy a maximum of 10% of our portfolio value on each position
  cerebro.addsizer(bt.sizers.AllInSizer, percents=10)
  
  
  # ADD DATA FEEDS TO BACKTRADER
  if prices is not None:
    print(f"DEBUG: Price data fetched...")
    for symbol in companies:
      price_data = prices[symbol].dropna(axis=0, how='all')
      # Get rid of invalid symbols or symbols with with insuficient historical data
      if len(price_data) > minimum_data_required:
        data = bt.feeds.PandasData(dataname=price_data)
        cerebro.adddata(data=data, name=symbol)
        print(f"Added datafeed for {symbol}, {len(price_data)}")
  else:
    print(f"Aborted: No price data fetched, please check ticker symbols")
  
  run_result = cerebro.run()
  print('\n\nEnding Portfolio Value: %.2f' % cerebro.broker.getvalue())
  
  # Plotting only works with a few companies
  #cerebro.plot(start=datetime.strptime(apply_strategy_on, "%Y-%m-%d"))
  
  print(f"End of backtest")

