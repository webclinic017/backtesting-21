# Backtrader for NASDAQ stocks

Work in progress... No Documentation yet!  
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



## Strategy
The file ``strategy_01.py`` contains the code loop to execute the strategy (including a custom indicator). Change this file to use your own strategy.  
This strategy uses a ``bracket_order`` to buy at market value, automatically sets a stop lost based on 2*ATR and a take profit value based on a 1.5 times risk to reward ratio. Also this strategy will close position after a position has been held for a maximum od 20 days. (We assume the historical prices data is a daily timeframe)  

## Backtrader documentation
[Package documentation](https://www.backtrader.com/docu/)


## Installation  
Make sure [git](https://gitforwindows.org/) and [python 3+](https://www.python.org/downloads/) are installed on your machine  
- ``git clone git@github.com:poivronjaune/backtesting.git`` using SSH  
or  
- ``git clone https://github.com/poivronjaune/backtesting.git`` using HTTPS  
  
- ``cd backtesting``  
- ``python -m venv env``  or ``py -m venv env``  
- ``env\Scripts\Activate`` (windows)  
- ``python -m pip install --upgrade pip`` or ``py -m pip install --upgrade pip``  
- ``pip install -r requirements.txt``  
  
tip: removing all packages from virtual environment  
- ``pip freeze > remove.txt``  
- ``pip install``  
  
  
## Running
Adjust your symbols list by changing this line ``companies = transportation["Symbol"].to_list()``  using one of the list from the predefined datasets
Run the script using ``python app.py``  

A folder named LOG_CSV will contain a csv log file ``csv_log-datetime.csv`` of how the strategy was applied. Use a spreadsheet to import, filter and analyse your results. A ``log_to_csv`` flag set to False can prevent the creation of this csv file.


#### Custom indicator credit  
mementum's github [repo](https://github.com/mementum/backtrader/pull/374/files)
