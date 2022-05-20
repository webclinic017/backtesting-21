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

# Extract a bunch of historical data and return a multi-index dataframe
def get_prices_for(yahoo_symbol, start_date="2019-01-01", end_date=None): 
  if end_date is None:
    end_date = str(datetime.now().strftime("%Y-%m-%d"))
    
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
  
  ARKK_funds = dict()
  ARKK_funds["ark_innovation"] = ARKK_fund["Symbol"].to_list()

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
  NASDAQ_dict["nasdaq_all"]               = nasdaq_companies["Symbol"].to_list()
  NASDAQ_dict["nasdaq_basic_industies"]   = basic_industries["Symbol"].to_list()
  NASDAQ_dict["nasdaq_capital_goods"]     = capital_goods["Symbol"].to_list()
  NASDAQ_dict["nasdaq_consumer_durable"]  = consumer_durable["Symbol"].to_list()
  NASDAQ_dict["nasdaq_consumer_non_dur"]  = consumer_non_dur["Symbol"].to_list()
  NASDAQ_dict["nasdaq_consumer_services"] = consumer_services["Symbol"].to_list()
  NASDAQ_dict["nasdaq_energy"]            = energy["Symbol"].to_list()
  NASDAQ_dict["nasdaq_finance"]           = finance["Symbol"].to_list()
  NASDAQ_dict["nasdaq_health_care"]       = health_care["Symbol"].to_list()
  NASDAQ_dict["nasdaq_miscellaneous"]     = miscellaneous["Symbol"].to_list()
  NASDAQ_dict["nasdaq_public_utilities"]  = public_utilities["Symbol"].to_list()
  NASDAQ_dict["nasdaq_technology"]        = technology["Symbol"].to_list()
  NASDAQ_dict["nasdaq_transportation"]    = transportation["Symbol"].to_list()

  return NASDAQ_dict

def test_symbols():
  # testccompanies = ['ORCL', 'AAPL', 'GATEU']
  manual_groups = dict()
  manual_groups["test_1"] = ['ORCL', 'AAPL', 'GATEU']

  return manual_groups

def default_setup():
    app_params = {
      "start_historical_data" : "2018-01-01",                          # Historical data start_date
      "end_historical_data"   : datetime.today().strftime('%Y-%m-%d'),   # Historical data end_date,
      "start_apply_strategy"  : "2021-01-01",                           # Strategy apply date (skip price data before this date)
      "end_apply_strategy"    : datetime.today().strftime('%Y-%m-%d'),
      "minimum_data_required" : 300,
      "sector"                : "test_1",
      "start_cash"            : 3000,
      "commission"            : 0.001,
      "max_hold_days"         : 10,
      "risk_to_reward"        : 1.53
    }
    return app_params

def main(show_gui=False):
  symbol_groups = NASDAQ() | ARKK_funds() | test_symbols()
  app_params = default_setup()
  
  # TODO: Implement UI later
  # # Get inout from desktop GUI
  # if show_gui == "desktop":
  #   app_params = GUI.show_gui(True)
  # elif show_gui == "browser":
  #   pass
  #   # NOT IMPLEMENTED
  #   # app_params = WEB.show_web(True)

  
  # Setup backtest variabales to call cerebro.run()
  start_of_price_data   = app_params["start_historical_data"]           # Historical data start_date
  end_of_price_data     = app_params["end_historical_data"]             # Historical data end_date
  apply_strategy_on     = app_params["start_apply_strategy"]            # Strategy apply date (skip price data before this date)
  minimum_data_required = app_params["minimum_data_required"]           # Minimum price data that must be fetched for strategy to work
  start_cash            = app_params["start_cash"]
  broker_commission     = app_params["commission"]
  max_hold_days         = app_params["max_hold_days"]
  risk_to_reward        = app_params["risk_to_reward"]
  
  companies = symbol_groups[app_params['sector']]
  print(f"Fetching price data for {len(companies)} symbols")
  prices = get_prices_for(companies, start_date=start_of_price_data, end_date=end_of_price_data)
  
  # SETUP Backtrader portfolio info and commisions
  cash = start_cash
  commission = broker_commission
  cerebro = bt.Cerebro(tradehistory=True)
  cerebro.broker.set_cash(cash)
  cerebro.broker.setcommission(commission=commission)
  cerebro.addsizer(bt.sizers.AllInSizer, percents=20)                           
  print('\n\nStarting Portfolio Value: %.2f' % cerebro.broker.getvalue())
  
  # SETUP a strategy to run on our data
  cerebro.addstrategy(strategy_01, apply_date=apply_strategy_on, risk_to_reward=risk_to_reward, max_hold=max_hold_days)
 
  # ADD DATA FEEDS TO BACKTRADER
  if prices is not None:
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

  print(f"\n\nEnding Portfolio Value: {cerebro.broker.getvalue()}")

  print(f"End of backtest")


if __name__ == "__main__":
  if "-gui" in sys.argv:
    gui_interface = "desktop"
  else:
    gui_interface = None
    
  main(show_gui=gui_interface)

