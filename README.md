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
This strategy uses a ``bracket_order`` to buy at market value, automatically sets a stop lost based on 2*ATR and a take profit value based on a 1.5 times risk to reward ratio.  

## Backtrader documentation
[Package documentation](https://www.backtrader.com/docu/)


## Installation  
``python venv env``  
``python -m pip install --upgrade pip``  
``pip install -r requirements.txt``  

## Running
Adjust your symbols list by changing this line ``companies = transportation["Symbol"].to_list()``  using one of the list from the predefined datasets
Run the script using ``python app.py``  

A log file ``log_strategy-date-time.txt`` will be created to see how the strategy was applied. The screen log can be turned off using the ``log_to_screen=False`` parameter in the ``cerebro.addstrategy(log_to_screen=False)`` command.


#### Custom indicator credit  
mementum's github [repo](https://github.com/mementum/backtrader/pull/374/files)
