from datetime import datetime, timedelta, date
from wsgiref import headers
import backtrader as bt

class StrategyLogger():

  # TODO: Implement a log file header that is based on the indicators that were added in the strategy
  #       Loop on the keys of the indicators data

  def __init__(self, logname="default", seperator=";"):
    # Commun seperator for all log files
    self.seperator = seperator
    # SETUP NOTIFY_ORDER LOG FILE
    self.header   = "date;log_type;symbol;open;high;low;close;volume;order_ref;order_name;order_type;order_status;order_price;order_size;order_value;order_commission;max_hold_date;EMA200;EMA20;ATR;SuperTrend"
    self.order_filename = f"LOG_CSV\O-{logname}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"      
    try:
      self.log_order = open(f"{self.order_filename}","w")
      self.log_order.write(f"{self.header}\n")
      
    except Exception as e:
      self.log_order = None

    # SETUP TRADES LOG FILE
    self.trade_header = "date;ref;symbol;trade_status;size;price;value;commission;pnl;pnlcomm;justopened;isopen;isclosed;baropen;dtopen;barclose;dtclose;barlen;status;buy_open;buy_close;sell_open;sell_close"
    self.trade_filename = f"TRADES\T-{logname}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"      
    try:
      self.log_trade = open(f"{self.trade_filename}","w")
      self.log_trade.write(f"{self.trade_header}\n")
    except Exception as e:
      self.log_trade = None

    # SETUP STRATEGY PLACED_ORDER LOG FILE
    placed_order_path = "PLACED"
    self.placed_order_filename = f"{placed_order_path}\P-{logname}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
    with open(f"{placed_order_path}\csv_header.txt","r") as f:
      header = f.read()
      f.close()
    placed_orders_header = header

    try:
      self.log_placed = open(f"{self.placed_order_filename}","w")
      self.log_placed.write(f"{placed_orders_header}\n")
    except Exception as e:
      self.log_placed = None

    return
    
  def log_order_to_csv(self, data=None, indicators=None, max_hold_dates= None, log_type=None, order=None, order_data=None):
    ''' Logging function to produce a CSV file of ORDERS for later import and analysis 
        date;log_type;symbol;open;high;low;close;volume;order_ref;order_name;order_status;order_price;order_size;order_value;order_commission;max_hold_date;EMA200;EMA20;ATR;SuperTrend
    '''
    if self.log_order is None:
      return

    symbol_data = None
    if data is not None:
      symbol_data = data
    
    if order is not None:
      symbol_data = order.data

    if symbol_data is not None:
      dt = symbol_data.datetime.date(0)
      date_str   = f"{dt.isoformat()}"
      symbol_str = f"{symbol_data._name}"
      open_str   = f"{symbol_data.open[0]:.2f}"
      high_str   = f"{symbol_data.high[0]:.2f}"
      low_str    = f"{symbol_data.low[0]:.2f}"
      close_str  = f"{symbol_data.close[0]:.2f}"
      volume_str = f"{symbol_data.volume[0]:.0f}"

      if max_hold_dates is not None:
        max_hold_date_str = f"{'' if max_hold_dates[symbol_data._name] == None else max_hold_dates[symbol_data._name]}"
      else:
        max_hold_date_str = ''

      # TODO: Replace wity a loop thourgh indicators keys
      EMA200_str     = f"{indicators[symbol_data]['ema2'][0]:.2f}"
      EMA20_str      = f"{indicators[symbol_data]['ema1'][0]:.2f}"
      ATR_str        = f"{indicators[symbol_data]['atr'][0]:.2f}"
      supertrend_str = f"{indicators[symbol_data]['supertrend'][0]:.2f}"
    else:
      # Something's wrong bad data available
      raise ValueError("Bad Indicator data found.")
      #return

    if log_type is not None:
      log_type   = f"{log_type}"
    else:
      log_type   = ""

    if order is not None:
      order_ref_str    = f"{order.ref}"
      order_name_str   = f"{order.getordername()}"
      order_type_str   = f"{order.ordtypename()}"
      order_status_str = f"{order.getstatusname()}"
      order_trade_id_str = f"{order.tradeid}"           # Not useful keep comment to remember we tried it (almost always zero, changes on overlaping order for same asset)
    else:
      order_ref_str    = ""
      order_name_str   = ""
      order_type_str   = ""
      order_status_str = ""
      order_trade_id_str = f"-1"

    if order_data is not None:
      order_price_str  = f"{order_data.price:.2f}"
      order_size_str   = f"{order_data.size:.2f} "
      order_value_str  = f"{order_data.value:.2f}"
      order_comm_str   = f"{order_data.comm:.2f} "
    else:
      order_price_str  = f""
      order_size_str   = f""
      order_value_str  = f""
      order_comm_str   = f""

    sep = self.seperator
    empty_str = ""
    # TODO: Implement log_str for indicators based in keys available in indicators data
    # Align string with self.header in __init_ method
    log_str  = f"{date_str}{sep}{log_type}{sep}{symbol_str}{sep}{open_str}{sep}{high_str}{sep}{low_str}{sep}{close_str}{sep}{volume_str}{sep}"
    log_str += f"{order_ref_str}{sep}{order_name_str}{sep}{order_type_str}{sep}{order_status_str}{sep}{order_price_str}{sep}{order_size_str}{sep}{order_value_str}{sep}{order_comm_str}{sep}{max_hold_date_str}{sep}"
    log_str += f"{EMA200_str}{sep}{EMA20_str}{sep}{ATR_str}{sep}{supertrend_str}{sep}{order_trade_id_str}{sep}\n"
    self.log_order.write(log_str)

  def log_trade_to_csv(self, trade=None):
    ''' Logging function to produce a CSV file of TRADES for later import and analysis 
        date;log_type;symbol;trade_status;open;high;low;close;volume;order_ref;order_name;order_status;order_price;order_size;order_value;order_commission;max_hold_date;EMA200;EMA20;ATR;SuperTrend
    '''
    if self.log_trade is None:
      return

    if trade is None:
      return

    sep = self.seperator
    date_trade = trade.data.datetime.date(0)
    trade_status = trade.status
    trade_history_len = len(trade.history)
    trade_symbol = trade.data._name
    buy_index = trade.baropen - 1
    buy_open  = trade.data._dataname.Open[buy_index]
    buy_close = trade.data._dataname.Close[buy_index]


    if trade.isclosed:
      trade_close_date = trade.close_datetime()
      trade_close_bar  = trade.barclose
      trade_bar_len    = trade.barlen
      sell_index = trade.barclose - 1
      sell_open  = trade.data._dataname.Open[sell_index]
      sell_close = trade.data._dataname.Close[sell_index]      
    else:
      trade_close_date = ""
      trade_close_bar  = ""
      trade_bar_len    = ""
      sell_open        = ""
      sell_close       = ""

    log_str  = f"{date_trade}{sep}{trade.ref}{sep}{trade_symbol}{sep}{trade_status}{sep}{trade.size:.2f}{sep}{trade.price:.2f}{sep}{trade.value:.2f}{sep}{trade.commission:.4f}{sep}"
    log_str += f"{trade.pnl:.2f}{sep}{trade.pnlcomm:.4f}{sep}{trade.justopened}{sep}{trade.isopen}{sep}{trade.isclosed}{sep}"
    log_str += f"{trade.baropen}{sep}{trade.open_datetime()}{sep}{trade_close_bar}{sep}{trade_close_date}{sep}{trade_bar_len}{sep}{trade.status}{sep}"
    log_str += f"{buy_open:.2f}{sep}{buy_close:.2f}{sep}"
    log_str += f"{sell_open}{sep}{sell_close}{sep}"
    log_str += f"\n"
#   self.trade_header = "date;ref;symbol;size;price;value;commission;
#                        pnl;pnlcomm;justopened;isopen;isclosed;baropen;dtopen;barclose;dtclose;barlen;
#                        buy_open;buy_close;buy_size;buy_value;"
#                        sell_open;sell_close;sell_size;sell_value
    self.log_trade.write(log_str)

  def return_order_as_csv_string(self, order):
    sep = self.seperator
    #dt = symbol_data.datetime.date(0)
    
    order_str  = f""
    order_str += f"{order.ref}{sep}"
    order_str += f"{order.getordername()}{sep}"
    order_str += f"{order.ordtypename()}{sep}"
    order_str += f"{order.getstatusname()}{sep}"
    order_data = order.executed if order.status in [order.Completed, order.Partial, order.Cancelled, order.Expired] else order.created
    # BUG : Not using the expired or canceled or executed date
    buy_dt = bt.num2date(order_data.dt).date()
    order_str += f"{buy_dt.isoformat()}{sep}"
    order_str += f"{order_data.size:.2f}{sep}"
    order_str += f"{order_data.price:.2f}{sep}"
    order_str += f"{order_data.value:.2f}{sep}"
    order_str += f"{order_data.comm:.2f}{sep}"
    order_str += f"{order_data.pnl:.2f}{sep}"
    order_str += f"{order_data.psize:.2f}{sep}"
    order_str += f"{order_data.pprice:.2f}{sep}"

    print(f"DEBUG ORDER_DATA ->\nStatus:{order.status}\ndata:{order_data}") 
    print(f"--------------------------------------")
    print(f"Order.Completed :{order.Completed}")
    print(f"Order.Partial   :{order.Partial}")
    print(f"Order.Submitted :{order.Submitted}")
    print(f"Order.Accepted  :{order.Accepted}")
    print(f"Order.Rejected  :{order.Rejected}")
    print(f"Order.Margin    :{order.Margin}")
    print(f"Order.Cancelled :{order.Cancelled }")
    print(f"Order.Canceled  :{order.Canceled}")
    print(f"Order.Expired   :{order.Expired}")
    print(f"--------------------------------------\n")
    print(f"DEBUG ORDER_DATA (Dir)\n{dir(order_data)}")
    return order_str

  def return_signal_data_as_csv_str(self, signal_data):
    sep = self.seperator
    signal_str  = f""
    signal_str += f"{signal_data.get('signal_dt')}{sep}"
    signal_str += f"{signal_data.get('buy_price'):.2f}{sep}"
    signal_str += f"{signal_data.get('stop_loss'):.2f}{sep}"
    signal_str += f"{signal_data.get('take_profit'):.2f}{sep}"
    signal_str += f"{signal_data.get('max_hold_dt')}{sep}"
    signal_str += f"{signal_data.get('open'):.2f}{sep}"
    signal_str += f"{signal_data.get('high'):.2f}{sep}"
    signal_str += f"{signal_data.get('low'):.2f}{sep}"
    signal_str += f"{signal_data.get('close'):.2f}{sep}"
    signal_str += f"{signal_data.get('volume'):.0f}{sep}"

    return signal_str

  def log_placed_order(self, strat_trades=None):
    if strat_trades is None:
      return

    sep = self.seperator
    placed_trades_header  = f"id;symbol;"
    placed_trades_header += f"market_ref;"
    placed_trades_header += f"stop_limit_ref;"
    placed_trades_header += f"take_profit_ref;"
    placed_trades_header += f"\n"
    #self.log_placed.write(placed_trades_header)

    for trade in strat_trades:
      placed_trade_id = trade["id"]
      symbol = trade["symbol"]
      signal_data  = trade['signal']
      buy_order    = trade['market_buy']
      stop_order   = trade['stop_limit']
      target_order = trade['take_profit']
      if "close_position" in trade:
        close_order = trade["close_position"]
      else:
        close_order = None

      log_str  = f"{placed_trade_id}{sep}{symbol}{sep}"
      log_str += self.return_signal_data_as_csv_str(signal_data)
      log_str += self.return_order_as_csv_string(buy_order)
      log_str += self.return_order_as_csv_string(stop_order)
      log_str += self.return_order_as_csv_string(target_order)

      if close_order is not None:
        log_str += self.return_order_as_csv_string(close_order)
  
      log_str += f"\n"
      self.log_placed.write(log_str)
# order_ref;order_name;order_type;order_status;order_price;order_size;order_value;order_commission;max_hold_date;

    #print(f"DEBUG LOG PLACED ORDER : trades type : {type(strat_trades)}, trades_len:{len(strat_trades)}")
    
    
  def close(self):
      self.log_order.close()
      self.log_trade.close()
      self.log_placed.close()
#      