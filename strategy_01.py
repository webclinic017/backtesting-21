from datetime import datetime, timedelta, date
import backtrader as bt

from strategy_logger import *
from custom_indicators import *
from strategy_logger import StrategyLogger

# TODO: Convert this function to a class or integrate into the logger class
def progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='>'):
  percent       = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration/float(total)))
  filled_length = int(length * iteration // total) # // = floor when dividing
  bar = fill * filled_length + '-' * (length - filled_length)
  print(f'\r{prefix}[{bar}]  {percent}% {suffix}', end='')
  if iteration == total:
    print()


class strategy_01(bt.Strategy):
  # self.params or self.p (are identical)
  # Stop loss set to supertrend lower band
  params = (
      ('apply_date', '2021-01-01'),
      ('risk_to_reward', 1.5),
      ('max_hold', 10),
      ('log_to_csv', True),
      ('ema1', 20),
      ('ema2', 200),
      ('atr', 14),
      ('stperiod', 10),
  )

  def __init__(self):
    # Create defaut log files (TODO: adapt to create only when flags are true)
    if self.p.log_to_csv:
      self.csv_logger = StrategyLogger(logname="log_01", seperator=";")

    #progress_bar_prefix = 'Indicators setup'.ljust(20, ' ')
    #progress_bar(0, len(self.datas), prefix=progress_bar_prefix, suffix='Complete', length=50, fill="*")
    
    # Keep a copy of the current data being processed in NEXT Loop
    self.price_data = None

    # Property to store the maximum hold date of a position by symbol data based on buy time
    self.max_hold_dates = dict()

    # Property to store all indicators by symbol data
    self.inds = dict()

    #print(f"Len of self.datas: {len(self.datas)}")
    for i, d in enumerate(self.datas):
      #progress_bar_prefix = f'Indicators {d._name.upper()}'.ljust(20, ' ')
      #progress_bar(i+1, len(self.datas), prefix=progress_bar_prefix, suffix='Complete', length=50, fill="*")
      self.inds[d] = dict()
      self.inds[d]['ema1']       = bt.indicators.ExponentialMovingAverage(d.close, period=self.params.ema1)  # Short EMA 20
      self.inds[d]['ema2']       = bt.indicators.ExponentialMovingAverage(d.close, period=self.params.ema2)  # Long  EMA 200
      self.inds[d]['atr']        = bt.indicators.AverageTrueRange(d, period=self.params.atr)
      self.inds[d]['supertrend'] = SuperTrend(d, period=self.params.stperiod)


  # STRATEGY FUNCTIONS
  def notify_order(self, order):
    order_data = order.executed if order.status in [order.Completed, order.Partial] else order.created
    self.csv_logger.log_order_to_csv(max_hold_dates=self.max_hold_dates, indicators=self.inds, log_type="NOTIFY_ORDER", order=order, order_data=order_data)

  def notify_trade(self, trade):
    if not trade.isclosed:
      return
    self.csv_logger.log_trade_to_csv(trade=trade)
    print(f"DEBUG_TRADE: {trade}")
  

  def buy_conditions(self, data):
    cond_01 = data.close[0] > self.inds[data]['ema2'][0]                                                  # Price above EMA200
    cond_02 = self.inds[data]['supertrend'][0] < data.close[0]                                            # Supertrend is UP 
    cond_03 = (data.high[0] > self.inds[data]['ema1'][0]) and (data.low[0] < self.inds[data]['ema1'][0])  # Price crosses EMA20

    return cond_01 & cond_02 & cond_03

  def sell_conditions(self, data):
    # The only sell condition is if we hold our position for more time than max_hold_date
    if self.max_hold_dates[data._name] is not None:
      if data.datetime.date() >= self.max_hold_dates[data._name]:
        return True

    return False

  def next(self):
    # Skip some price values to start backtest at a specific date 
    start_strategy = datetime.strptime(self.params.apply_date, "%Y-%m-%d").date()
    if (self.datas[0].datetime.date(0) < start_strategy):
      # TODO: Add skip date progress bar
      return

    # Loop through each data set loaded for strategy
    dt = self.datetime.date()
    #progress_bar_prefix = f'Analysing {dt.isoformat()} : None'.ljust(40, ' ')
    #progress_bar(0, len(self.datas), prefix=progress_bar_prefix, suffix='Complete', length=75, fill="*")
    for i, d in enumerate(self.datas):
      pos = self.getposition(d).size
    
      #progress_bar_prefix = f'Analysing {dt.isoformat()} : {d._name.upper()}'.ljust(40, ' ')
      #progress_bar(i+1, len(self.datas), prefix=progress_bar_prefix, suffix='Complete', length=75, fill="*")

      log_action = "BUG"
      if not pos:
        if self.buy_conditions(d):
          buy_price   = d.close[0]
          stop_loss   = buy_price - 2 * self.inds[d]['atr'][0]
          take_profit = buy_price + (buy_price - stop_loss) * self.p.risk_to_reward
          max_hold_date = dt + timedelta(days=self.p.max_hold)
          self.max_hold_dates[d._name] = max_hold_date         
          orders = self.buy_bracket(d, stopprice=stop_loss, limitprice=take_profit, exectype=bt.Order.Market, valid=max_hold_date)          
          log_action = "LOG_BUY"
        else:
          self.max_hold_dates[d._name] = None
          log_action = "LOG_NEXT"
      else:
        if self.sell_conditions(d):
          self.close(d)
          self.max_hold_dates[d._name] = None
          log_action = "LOG_CLOSE"
        else:
          log_action = "LOG_NEXT"

      # Print results to csv_log   
      self.csv_logger.log_order_to_csv(data=d, max_hold_dates=self.max_hold_dates, indicators=self.inds, log_type=log_action)  

  def stop(self):
    for i, d in enumerate(self.datas):
      pos = self.getposition(d).size
      if pos:
        self.close(d)
        self.csv_logger.log_order_to_csv(data=d, max_hold_dates=self.max_hold_dates, indicators=self.inds, log_type="LOG_CLOSE")

    self.csv_logger.close()