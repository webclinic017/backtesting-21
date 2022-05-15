# Backtrader for NASDAQ stocks

Work in progress...  
This project is a learning experiment for backtesting using backtrader.  
Partial Documentation Only!  
Constructive comments on pythonic improvements or backtrader usage are welcomed.
   
## Datasets
Uses Datasets from [Stock Screener](https://github.com/poivronjaune/stock_screener/tree/main/DATASETS), Some predefined datasets :
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
  
Setup your own symbol's list in test_symbols() function available un app.py.
Add a new entry to the manuel_groups  
  ``manual_groups["test_1"] = ['ORCL', 'AAPL', 'GATEU']``
  ``manual_groups["yourname"] = ['symbol1', 'symbol2', 'etc..']``  
  See [issue-19](https://github.com/poivronjaune/backtesting/issues/19) to move this feature in a config file  



## Strategy
The file ``strategy_01.py`` contains the code loop to execute the strategy (including a custom indicator). Change this file to use your own strategy.  
This strategy uses a ``bracket_order`` to buy at market value, automatically sets a stop lost based on 2*ATR and a take profit value based on a 1.5 times risk to reward ratio. Also this strategy will close position after a position has been held for a maximum od 20 days. (We assume the historical prices data is a daily timeframe)  

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
  
## Notice
This project does not use the Backtrader built in observers or analysers as this was difficult to implement in a portfolio strategy that contains multiple assets (may upgrade this in future version)  

#### Custom indicator credit  
mementum's github [repo](https://github.com/mementum/backtrader/pull/374/files)
