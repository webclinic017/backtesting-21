# Backtrader for NASDAQ stocks

Work in progress...  
This project is a learning experiment for backtesting using [backtrader](https://www.backtrader.com/), a python backtesting package.  
Partial Documentation Only!  
Constructive comments on pythonic improvements or backtrader usage are welcomed.
   
## Datasets
Uses Datasets from [Stock Screener](https://github.com/poivronjaune/stock_screener/tree/main/DATASETS), Some predefined datasets (Jan 2022) :
- ARK Invest Innovation Fund indivudual companies
- nasdaq_companies 
- no_sector        
- basic_industries 
- capital_goods    
- consumer_durable 
- consumer_non_dur 
- consumer_services
- energy           
- finance          
- health_care      
- miscellaneous    
- public_utilities 
- technology       
- transportation   

## Strategy
The file ``strategy_01.py`` contains the code loop to execute the strategy (including a custom indicator). Change this file to use your own strategy.  
This strategy uses a ``bracket_order`` to buy at market value, automatically sets a stop lost based on 2*ATR and a take profit value based on a 1.5 times risk to reward ratio. Also this strategy will close position after a position has been held for a maximum of 10 days. (We assume the historical prices data is a daily timeframe)  

## Backtrader documentation
[Package documentation](https://www.backtrader.com/docu/)


## Installation  
Make sure [git](https://gitforwindows.org/) and [python 3+](https://www.python.org/downloads/) are installed on your machine  
- ``open a commad window``
- ``git clone git@github.com:poivronjaune/backtesting.git`` using SSH  
or  
- ``git clone https://github.com/poivronjaune/backtesting.git`` using HTTPS  
  
- ``cd backtesting``  
- ``python -m venv env``  or ``py -m venv env`` to create a virtual environment  
- ``env\Scripts\Activate`` (activate virtual environment on windows machines)  
- ``python -m pip install --upgrade pip`` or ``py -m pip install --upgrade pip``  
- ``pip install -r requirements.txt``  
  
tip: removing all packages from virtual environment  
- ``pip freeze > remove.txt``  
- ``pip uninstall -r remove.txt -y``  
  
  
## Running
The ``symbol_groups`` dictionnary contains a bunch of symbols grouped by name (considered a sector). More sectors can be added in the ``test_symbols()`` function.  

The ``default_setup()`` function contains all the strategy's parameters.  
The key ``"sector"`` will be used to select group of symbols to load from the ``symbol_groups`` dictionnary
  
run ``python app.py`` (make sure folders for logs are created : LOG_CSV, PLACED, TRADES)

## Results
3 LOG folders are available:
- LOG_CSV : logs [orders_info](https://www.backtrader.com/docu/order/) including [NOTIFY_ORDER](https://www.backtrader.com/docu/strategy/) events as the strategy places orders (submitted, accepted, completed)
- TRADES : logs all trade from NOTIFY_TRADE (see backtrader documentation [strategy](https://www.backtrader.com/docu/strategy/) and [trade info](https://www.backtrader.com/docu/trade/))
- PLACED : custom log with completed orders grouped by trade. Contains strategy's SIGNAL INFO, [BRACKET ORDER](https://www.backtrader.com/docu/order-creation-execution/bracket/bracket/) and CLOSE POSITION info when trade went longer that predfined MAX_HOLD_DAYS

Import logs to a google sheets or a microsoft spreadsheet to analyse performance  
  
## Parameters customisation  
```
def default_setup():
    app_params = {
      "start_historical_data" : "2018-01-01",                            
      "end_historical_data"   : datetime.today().strftime('%Y-%m-%d'),   
      "start_apply_strategy"  : "2021-01-01",                            
      "end_apply_strategy"    : datetime.today().strftime('%Y-%m-%d'),
      "minimum_data_required" : 300,
      "sector"                : "test_1",
      "start_cash"            : 3000,
      "commission"            : 0,
      "max_hold_days"         : 10,
      "risk_to_reward"        : 1.5
    }  
```    
The default setup will retreive historical data from "2018-01-01" to today.  
The backtest strategy will be applied strating from "2021-01-01" to today.  
Indicators require a minium of 200 rows of data so ``minimum_data_required``will skip any asset that retreived less prices values.  
The default "sector" that will be used is "test_1" from the ``test_symbols()`` function. Change this to customize your company symbols (trade tickers)
Starting cash for strategy is set to 3000$.  
Default commission are set to zero, this must be adjusted for your broker.  
The strategy will hold it's position for a maximum of 10 days.
The take_profit order will be set to 1.5 the stop_loss to have 1:1.5 Risk To Reward management scheme

Setup your own symbol's list in test_symbols() function available un app.py.
Add a new entry to the manuel_groups  
  ``manual_groups["test_1"] = ['ORCL', 'AAPL', 'GATEU']``
  ``manual_groups["yourname"] = ['symbol1', 'symbol2', 'etc..']``  
  See [issue-19](https://github.com/poivronjaune/backtesting/issues/19) to move this feature in a config file  


  
## Notice
This project does not use the Backtrader built in observers or analysers as this was difficult to implement in a portfolio strategy that contains multiple assets (may upgrade this in future version)  

#### Custom indicator credit  
mementum's github [repo](https://github.com/mementum/backtrader/pull/374/files)
