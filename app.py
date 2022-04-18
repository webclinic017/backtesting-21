# https://backtest-rookies.com/2017/08/22/backtrader-multiple-data-feeds-indicators/
import sys
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas_ta as ta
import backtrader as bt

import gui as GUI

from datetime import datetime, timedelta 
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

def ARKK_funds():
  # Innovation fund companies listed
  ARKK_fund = pd.read_csv("https://raw.githubusercontent.com/poivronjaune/stock_screener/main/DATASETS/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv")
  ARKK_fund.rename(columns={'ticker':'Symbol'}, inplace=True)
  ARKK_fund = ARKK_fund.dropna()
  
  ARKK_funds = ARKK_fund["Symbol"].to_list()

  return ARKK_funds

def NASDAQ():
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

  NASDAQ_dict = dict()
  NASDAQ_dict["all"]               = nasdaq_companies["Symbol"].to_list()
  NASDAQ_dict["basic_industies"]   = basic_industries["Symbol"].to_list()
  NASDAQ_dict["capital_goods"]     = capital_goods["Symbol"].to_list()
  NASDAQ_dict["consumer_durable"]  = consumer_durable["Symbol"].to_list()
  NASDAQ_dict["consumer_non_dur"]  = consumer_non_dur["Symbol"].to_list()
  NASDAQ_dict["consumer_services"] = consumer_services["Symbol"].to_list()
  NASDAQ_dict["energy"]            = energy["Symbol"].to_list()
  NASDAQ_dict["finance"]           = finance["Symbol"].to_list()
  NASDAQ_dict["health_care"]       = health_care["Symbol"].to_list()
  NASDAQ_dict["miscellaneous"]     = miscellaneous["Symbol"].to_list()
  NASDAQ_dict["public_utilities"]  = public_utilities["Symbol"].to_list()
  NASDAQ_dict["technology"]        = technology["Symbol"].to_list()
  NASDAQ_dict["transportation"]    = transportation["Symbol"].to_list()

  return NASDAQ_dict

def main(show_gui=False):
  ARKK_fund_list = ARKK_funds()
  NASDAQ_groups = NASDAQ()
  test_companies = ['ORCL', 'AAPL', 'GATEU']

  # Default backtest values
  app_params = {
      "start_historical_data":"2018-01-01",                          # Historical data start_date
      "end_historical_data":datetime.today().strftime('%Y-%m-%d'),   # Historical data end_date,
      "start_apply_strategy":"2021-01-01",                           # Strategy apply date (skip price data before this date)
      "end_apply_strategy":datetime.today().strftime('%Y-%m-%d'),
      "minimum_data_required":300,
      "sector":"test",
      "start_cash":3000,
      "commission":0.001
  }
  
  # Get inout from desktop GUI
  if show_gui == "desktop":
    app_params = GUI.show_gui(True)
  elif show_gui == "browser":
    pass
    #app_params = WEB.show_web(True)

  # Setup backtest variabales to call cerebro.run()
  start_of_price_data   = app_params["start_historical_data"]           # Historical data start_date
  end_of_price_data     = app_params["end_historical_data"]             # Historical data end_date
  apply_strategy_on     = app_params["start_apply_strategy"]            # Strategy apply date (skip price data before this date)
  minimum_data_required = app_params["minimum_data_required"]           # Minimum price data that must be fetched for strategy to work
  start_cash            = app_params["start_cash"]
  broker_commission     = app_params["commission"]
  
  print(f'DEBUG main(): {app_params}')

  if app_params["sector"] == "test":
    companies = test_companies
  elif app_params["sector"] == "ARKK Invest fund":
    companies = ARKK_fund_list
  else:
    sector = app_params["sector"]
    companies = NASDAQ_groups[f"{sector}"]

  print(f'DEBUG main() :\n{companies}')
  return

  print(f"Fetching price data for {len(companies)} symbols")
  prices = get_prices_for(companies, start_date=start_of_price_data, end_date=end_of_price_data)


  # SETUP Backtrader portfolio info and commisions
  cash = start_cash
  commission = broker_commission
  cerebro = bt.Cerebro()
  cerebro.broker.set_cash(cash)
  cerebro.broker.setcommission(commission=commission)
  print('\n\nStarting Portfolio Value: %.2f' % cerebro.broker.getvalue())
  
  # SETUP a strategy to run on our data
  cerebro.addstrategy(strategy_01, apply_date=apply_strategy_on, risk_to_reward=1.53, max_hold=20)
  
  # Buy a maximum of 10% of our portfolio value on each position
  cerebro.addsizer(bt.sizers.AllInSizer, percents=20)
  
  cerebro.addobserver(bt.observers.DrawDown)

  cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')
  cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DrawDown')
  cerebro.addanalyzer(bt.analyzers.Calmar, _name='Calmar')
  cerebro.addanalyzer(bt.analyzers.SQN, _name='SQN')

  # ADD DATA FEEDS TO BACKTRADER
  if prices is not None:
    print(f"DEBUG: Price data fetched...")
    plot_master_data = None
    for symbol in companies:
      price_data = prices[symbol].dropna(axis=0, how='all')
      # Get rid of invalid symbols or symbols with with insuficient historical data
      if len(price_data) > minimum_data_required:
        data = bt.feeds.PandasData(dataname=price_data)
        if plot_master_data is None:
          plot_master_data = data
          cerebro.adddata(data=data, name=symbol)
        else:
          data.plotinfo.plotmaster = plot_master_data
          cerebro.adddata(data=data, name=symbol)
        print(f"Added datafeed for {symbol}, {len(price_data)}")
  else:
    print(f"Aborted: No price data fetched, please check ticker symbols")
  

  if prices is not None:
    thestrats = cerebro.run()
    print(f"TheStrats: {len(thestrats)}\n")
    for thestart in thestrats:
      thestrat = thestrats[0]
      print(f"\nSharpe Ratio: {thestrat.analyzers.mysharpe.get_analysis()['sharperatio']}")


  print(f"\n\nEnding Portfolio Value: {cerebro.broker.getvalue()}")

  # Plotting only works with a few companies
  cerebro.plot(start=datetime.strptime(apply_strategy_on, "%Y-%m-%d"))
  #cerebro.plot()

  print(f"End of backtest")


if __name__ == "__main__":
  if "-gui" in sys.argv:
    gui_interface = "desktop"
  else:
    gui_interface = None
    
  main(show_gui=gui_interface)

