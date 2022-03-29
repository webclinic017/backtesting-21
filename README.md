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
The file ``strategy_01.py`` contains the code loop to execute the strategy (incuding some custom indicators). Change this file to use your own strategy.

## Backtrader documentation
[Package documentation](https://www.backtrader.com/docu/)


## Installation  
``python venv env``  
``python -m pip install --upgrade pip``  
``pip istall -r requirements.txt``  

## Running
Adjust your symbols list by changing this line ``companies = transportation["Symbol"].to_list()``
Run the script using ``python app.py``  

A log file ``log_strategy-date-time.txt`` will be creayed to see how the strategy was applied
