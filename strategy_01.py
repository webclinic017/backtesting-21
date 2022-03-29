from datetime import datetime, timedelta 
import backtrader as bt


# TODO: Move thos Indicator Code to a new files
class SuperTrendBand(bt.Indicator):
  """
  Helper inidcator for Supertrend indicator
  """
  params = (('period',10),('multiplier',3))
  lines = ('basic_ub','basic_lb','final_ub','final_lb')

  def __init__(self):
    self.l.atr = bt.indicators.AverageTrueRange(self.data, period=self.p.period)
    self.l.basic_ub = ((self.data.high + self.data.low) / 2) + (self.l.atr * self.p.multiplier)
    self.l.basic_lb = ((self.data.high + self.data.low) / 2) - (self.l.atr * self.p.multiplier)

  def next(self):
    if len(self)-1 == self.p.period:
      self.l.final_ub[0] = self.l.basic_ub[0]
      self.l.final_lb[0] = self.l.basic_lb[0]
    else:
      #=IF(OR(basic_ub<final_ub*,close*>final_ub*),basic_ub,final_ub*)
      if self.l.basic_ub[0] < self.l.final_ub[-1] or self.data.close[-1] > self.l.final_ub[-1]:
        self.l.final_ub[0] = self.l.basic_ub[0]
      else:
        self.l.final_ub[0] = self.l.final_ub[-1]

      #=IF(OR(baisc_lb > final_lb *, close * < final_lb *), basic_lb *, final_lb *)
      if self.l.basic_lb[0] > self.l.final_lb[-1] or self.data.close[-1] < self.l.final_lb[-1]:
        self.l.final_lb[0] = self.l.basic_lb[0]
      else:
        self.l.final_lb[0] = self.l.final_lb[-1]

class SuperTrend(bt.Indicator):
  """
  Super Trend indicator
  """
  params = (('period', 10), ('multiplier', 3))
  lines = ('super_trend',)
  plotinfo = dict(subplot=False)

  def __init__(self):
    self.stb = SuperTrendBand(self.data, period = self.p.period, multiplier = self.p.multiplier)

  def next(self):
    if len(self) - 1 == self.p.period:
      self.l.super_trend[0] = self.stb.final_ub[0]
      return

    if self.l.super_trend[-1] == self.stb.final_ub[-1]:
      if self.data.close[0] <= self.stb.final_ub[0]:
        self.l.super_trend[0] = self.stb.final_ub[0]
      else:
        self.l.super_trend[0] = self.stb.final_lb[0]

    if self.l.super_trend[-1] == self.stb.final_lb[-1]:
      if self.data.close[0] >= self.stb.final_lb[0]:
        self.l.super_trend[0] = self.stb.final_lb[0]
      else:
        self.l.super_trend[0] = self.stb.final_ub[0]



class strategy_RB(bt.Strategy):
  # self.params or self.p (are identical)
  # Stop loss set to supertrend lower band
  params = (
      ('apply_date', '2021-01-01'),
      ('risk_to_reward', 1.5),
      ('hold', 10),
      ('log_to_screen', False),
      ('log_to_file', True),
      ('ema1', 20),
      ('ema2', 200),
      ('atr', 14),
      ('stperiod', 10),
  )

  def log_next(self, data, action_str, dt=None):
    ''' Logging function for this strategy'''
    dt = dt or data.datetime.date(0)
    #log_str = f"{dt.isoformat()}, {data._name.ljust(6)} [Portfolio Value:{self.broker.getvalue():.2f}]{txt}\n"
    log_str  = f"{dt.isoformat()} LOG_ACTION   ["
    log_str += f"Symbol:{data._name}, "
    log_str += f"Position:{self.getposition(data).size:.2f}, "
    log_str += f"Price:{data.close[0]:.2f}, "
    log_str += f"EMA20(Blue):{self.inds[data]['ema1'][0]:.2f}, "
    log_str += f"EMA200(Yellow):{self.inds[data]['ema2'][0]:.2f}, "
    log_str += f"ATR:{self.inds[data]['atr'][0]:.2f}, "
    log_str += f"SuperTrend(Red/Green):{self.inds[data]['supertrend'][0]:.2f}"
    log_str += f"]"
    if action_str is not "None":
        log_str += f"\nAction: {data._name}, {action_str} "
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

  def __init__(self):
    if self.p.log_to_file:
      self.file_log = open(f"log_strategy-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt","w")

    self.inds = dict()
    print(f"Len of self.datas: {len(self.datas)}")
    for i, d in enumerate(self.datas):
      self.inds[d] = dict()
      self.inds[d]['ema1']       = bt.indicators.ExponentialMovingAverage(d.close, period=self.params.ema1)  # Short EMA 20
      self.inds[d]['ema2']       = bt.indicators.ExponentialMovingAverage(d.close, period=self.params.ema2)  # Long  EMA 200
      #self.inds[d]['cross']      = bt.indicators.CrossOver(self.inds[d]['ema1'],self.inds[d]['ema2'])
      self.inds[d]['atr']        = bt.indicators.AverageTrueRange(d, period=self.params.atr)
      self.inds[d]['supertrend'] = SuperTrend(d, period=self.params.stperiod)

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
          action_str = f"Buy:{buy_price:.2f},s:{stop_loss:.2f},t:{take_profit:.2f} "
      else:
        if self.sell_conditions(d):
          action_str = "Sell"

      # Print results to log
      self.log_next(d, action_str)

  def stop(self):
    self.close()
    self.file_log.close()