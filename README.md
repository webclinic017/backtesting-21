# Backtrader for NASDAQ stocks

Work in progress...  
This project is a learning experiment for backtesting using [backtrader](https://www.backtrader.com/), a python backtesting package. It is not investment advice.    
Partial Documentation Only!  
Constructive comments on pythonic improvements or backtrader usage are welcomed.
   
## Datasets
Uses Datasets from [Stock Screener](https://github.com/poivronjaune/stock_screener/tree/main/DATASETS), Some predefined datasets (Jan 2022) for NASDAQ and ARK INVEST :
- ark_innovation -> ARK Invest Innovation Fund indivudual companies        
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
- test   

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
  
## Configuration (in code)
The ``symbol_groups`` dictionnary contains a bunch of symbols grouped by name (considered a sector). More sectors can be added manually in the ``test_symbols()`` function.  

The ``default_setup()`` function contains all the strategy's parameters.  
The key ``"sector"`` will be used to select a group of symbols to load from the ``symbol_groups`` dictionnary. This value can be passed through a command line paramater ``py app.py -sector test``

The name of the log file is defined in the __init__() function of the ``strategy_logger.py``. Convention ``prefix-timestamp-suffix``
- ``prefix`` : Placed trades log with strategy id (default = P-log_01)
- ``timestamp`` : default datetime at file creation (default = year-month-dd-hours-minutes-seconds as yyyy-mm-dd-HH-MM-SS )
- ``suffix`` : no suffix contains the placed trades log, "-params" contains the strategie's parameters and a brief description, "-cash" contains the cash value log of portfolio before each trade execution

New strategies can be created as a seperate file and imported in the app.py, change the line ``cerebro.addstrategy`` to insert your specific strategy (see [backtrader documentation](https://www.backtrader.com/docu/strategy/) to define a new strategy)

## Running
 
  
run ``python app.py -sector test`` (make sure a folder for logs is created to store placed trades : PLACED)  
If no ``-sector`` flag supplied will default to ``test`` sector

## Results
- PLACED FOLDER contains 3 logs with a timestamp in filename.
- ``*-params.csv`` : strategy configuration and breif description of strategy being logged
- ``*-cash.csv`` : history of cash progression as strategy is executed on price data for multiple assets
- ``*-csv`` : custom log with all completed orders grouped by trade. It contains the strategy's SIGNAL INFO, [BRACKET ORDER](https://www.backtrader.com/docu/order-creation-execution/bracket/bracket/) and CLOSE POSITION info when trade went longer that predfined in MAX_HOLD_DAYS

Import logs to a google sheets or a microsoft spreadsheet to analyse performance.
  
## Parameters customisation  
```
def default_setup():
    app_params = {
      "start_historical_data" : "2018-01-01",                            
      "end_historical_data"   : datetime.today().strftime('%Y-%m-%d'),   
      "start_apply_strategy"  : "2021-01-01",                            
      "end_apply_strategy"    : datetime.today().strftime('%Y-%m-%d'),
      "minimum_data_required" : 300,
      "start_cash"            : 3000,
      "commission"            : 0,
      "max_hold_days"         : 10,
      "risk_to_reward"        : 1.5
    }  
```    
The default setup will retreive historical data from "2018-01-01" to today.  
The backtest strategy will be applied strating from "2021-01-01" to today.  
Indicators require a minium of 200 rows of data so ``minimum_data_required``will skip any asset that retreived less prices values tham required for indicators (ex:ema200 needs at least 200 days of data).  
The default "sector" that will be used is "test_1" from the ``test_symbols()`` function. Change this to customize your company symbols (trade tickers)
Starting cash for strategy is set to 3000$.  
Default commission is set to 0.001 (0.1%), this must be adjusted for your broker.  
The strategy will hold it's position for a maximum of 10 days.
The take_profit order will be set to 1.5 the stop_loss to have 1:1.5 Risk To Reward management scheme

Setup your own symbol's list in test_symbols() function defined in app.py.
Add a new entry to the manuel_groups  
  ``manual_groups["test"] = ['ORCL', 'AAPL', 'GATEU']``
  ``manual_groups["yourname"] = ['symbol1', 'symbol2', 'etc..']``  
  See [issue-19](https://github.com/poivronjaune/backtesting/issues/19) to move this feature in a config file  


  
## Notice
This project does not use the Backtrader built in observers or analysers as this was difficult to implement in a portfolio strategy that contains multiple assets (may upgrade this in future version)  

#### Custom indicator credit  
mementum's github [repo](https://github.com/mementum/backtrader/pull/374/files)
