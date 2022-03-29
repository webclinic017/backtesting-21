from datetime import datetime, timedelta, date
import backtrader as bt

from custom_indicators import *

class strategy_RB(bt.Strategy):
  # self.params or self.p (are identical)
  # Stop loss set to supertrend lower band
  params = (
      ('apply_date', '2021-01-01'),
      ('risk_to_reward', 1.5),
      ('hold', 10),
      ('log_to_screen', False),
      ('log_to_file', True),
      ('log_to_csv', True),
      ('ema1', 20),
      ('ema2', 200),
      ('atr', 14),
      ('stperiod', 10),
  )

  def __init__(self):
    # TODO: Adjust to respect log flags and not create non required files
    # Create log default files
    if self.p.log_to_file:
      self.file_log = open(f"LOG_TXT\log_strategy-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt","w")
      self.csv_log  = open(f"LOG_CSV\csv_log-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt","w")
      self.csv_log.write(f"date;log_type;symbol;position;open;high;low;close;volume;order_ref;order_name;order_status;price;stop_loss;target;EMA200;EMA20;ATR;SuperTrend\n")

    self.inds = dict()
    print(f"Len of self.datas: {len(self.datas)}")
    for i, d in enumerate(self.datas):
      self.inds[d] = dict()
      self.inds[d]['ema1']       = bt.indicators.ExponentialMovingAverage(d.close, period=self.params.ema1)  # Short EMA 20
      self.inds[d]['ema2']       = bt.indicators.ExponentialMovingAverage(d.close, period=self.params.ema2)  # Long  EMA 200
      #self.inds[d]['cross']      = bt.indicators.CrossOver(self.inds[d]['ema1'],self.inds[d]['ema2'])
      self.inds[d]['atr']        = bt.indicators.AverageTrueRange(d, period=self.params.atr)
      self.inds[d]['supertrend'] = SuperTrend(d, period=self.params.stperiod)



  # LOG FUNCTIONS
  def log_to_csv(self, data=None, indicators= None, log_type=None, order=None, order_data=None):
    ''' Logging function to produce a CSV file for later import and analysis 
        date;log_type;symbol;position;open;high;low;close;volume;order_ref;order_name;order_status;price;stop_loss;target;EMA200;EMA20;ATR;SuperTrend
    '''
    if data is not None:
      dt = data.datetime.date(0)
      date_str     = f"{dt.isoformat()}"
      symbol_str   = f"{data._name}"
      position_str = f"{self.getposition(data).size:.2f}"
      open_str     = f"{data.open[0]}"
      high_str     = f"{data.high[0]}"
      low_str      = f"{data.low[0]}"
      close_str    = f"{data.close[0]}"
      volume_str   = f"{data.volume[0]}"
    else:
      date_str     = ""
      symbol_str   = ""
      position_str = ""
      open_str     = ""
      high_str     = ""
      low_str      = ""
      close_str    = ""
      volume_str   = ""

    if log_type is not None:
      log_type   = f"{log_type}"
    else:
      log_type   = ""

    sep = ";"
    empty_str = ""
    log_str  = f"{date_str}{sep}{log_type}{sep}{symbol_str}{sep}{position_str}{sep}{open_str}{sep}{high_str}{sep}{low_str}{sep}{close_str}{sep}{volume_str}{sep}"
    log_str += f"{empty_str}{sep}{empty_str}{sep}{empty_str}{sep}{empty_str}{sep}{empty_str}{sep}{empty_str}{sep}"
    log_str += f"{empty_str}{sep}{empty_str}{sep}{empty_str}{sep}{empty_str}{sep}\n"
    #self.csv_log.write(log_str)

    # order_ref;order_name;order_status;price;stop_loss;target;
    # EMA200;EMA20;ATR;SuperTrend



  def log_next(self, data, dt=None):
    ''' Logging function for this strategy'''
    dt = dt or data.datetime.date(0)
    #log_str = f"{dt.isoformat()}, {data._name.ljust(6)} [Portfolio Value:{self.broker.getvalue():.2f}]{txt}\n"
    log_str  = f"{dt.isoformat()} LOG_NEXT     ["
    log_str += f"Symbol:{data._name}, "
    log_str += f"Position:{self.getposition(data).size:.2f}, "
    log_str += f"Price:{data.close[0]:.2f}, "
    log_str += f"EMA20(Blue):{self.inds[data]['ema1'][0]:.2f}, "
    log_str += f"EMA200(Yellow):{self.inds[data]['ema2'][0]:.2f}, "
    log_str += f"ATR:{self.inds[data]['atr'][0]:.2f}, "
    log_str += f"SuperTrend(Red/Green):{self.inds[data]['supertrend'][0]:.2f}"
    log_str += f"]"
    log_str += f"\n"

    if self.p.log_to_screen:
      print(log_str)
    if self.p.log_to_file:
      self.file_log.write(log_str)

  def log_buy(self, data, action_str, dt=None):
    dt = dt or data.datetime.date(0)
    #log_str = f"{dt.isoformat()}, {data._name.ljust(6)} [Portfolio Value:{self.broker.getvalue():.2f}]{txt}\n"
    log_str  = f"{dt.isoformat()} BUY_SIGNAL   ["
    log_str += f"Symbol:{data._name}, "
    log_str += f"Position:{self.getposition(data).size:.2f}, "
    log_str += f"Action: {action_str} "
    log_str += f"]"
    log_str += f"\n"

    if self.p.log_to_screen:
      print(log_str)
    if self.p.log_to_file:
      self.file_log.write(log_str)


  def log_order(self, order, order_data):
      dt = order.data.datetime.date(0)
      log_str  = f"{dt.isoformat()} NOTIFY_ORDER ["
      log_str += f"Symbol:{order.data._name},"
      log_str += f"Ref:{order.ref},"
      log_str += f"Name:{order.getordername()},"
      log_str += f"Type:{order.ordtypename()}"
      log_str += f"Status:{order.getstatusname()},"
      log_str += f"Price:{order_data.price:.2f},"
      log_str += f"Size:{order_data.size:.2f},"
      log_str += f"Value:{order_data.value:.2f},"
      log_str += f"Comm:{order_data.comm:.2f}"
      log_str += f"]\n"
      if self.p.log_to_screen:
        print(log_str)    
      if self.p.log_to_file:
        self.file_log.write(log_str)


  # STRATEGY FUNCTIONS
  def notify_order(self, order):
    order_data = order.executed if order.status in [order.Completed, order.Partial] else order.created
    self.log_order(order, order_data)

  def buy_conditions(self, data):
    cond_01 = data.close[0] > self.inds[data]['ema2'][0]                                                  # Price above EMA200
    cond_02 = self.inds[data]['supertrend'][0] < data.close[0]                                            # Supertrend is UP 
    cond_03 = (data.high[0] > self.inds[data]['ema1'][0]) and (data.low[0] < self.inds[data]['ema1'][0])  # Price crosses EMA20

    return cond_01 & cond_02 & cond_03

  def sell_conditions(self, data):
    return False

  def next(self):
    # Skip some price values to start backtest at a specific date 
    start_strategy = datetime.strptime(self.params.apply_date, "%Y-%m-%d").date()
    if (self.datas[0].datetime.date(0) < start_strategy):
      return

    # Loop through each data set loaded for strategy
    for i, d in enumerate(self.datas):
      dt, dn = self.datetime.date(), d._name
      pos = self.getposition(d).size
    
      action_str = "None"
      if not pos:
        if self.buy_conditions(d):
          buy_price   = d.close[0]
          stop_loss   = buy_price - 2 * self.inds[d]['atr'][0]
          take_profit = buy_price + (buy_price - stop_loss) * self.p.risk_to_reward
          
          #orders = self.buy_bracket(price=buy_price, valid=self.max_hold_date, stopprice=stop_loss, limitprice=take_profit)          
          orders = self.buy_bracket(d, stopprice=stop_loss, limitprice=take_profit)          
          action_str = f"Estimated Market Price:{buy_price:.2f}, Stop:{stop_loss:.2f}, Target:{take_profit:.2f} "
          self.log_buy(d, action_str)
      else:
        if self.sell_conditions(d):
          action_str = "Sell"

      # Print results to log
      self.log_next(d)

  def stop(self):
    self.file_log.close()