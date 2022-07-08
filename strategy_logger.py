from datetime import datetime, timedelta, date
import backtrader as bt

# VERY SPECIFIC LOGGER, Needs improvements to become generic
class StrategyLogger():
  
  def __init__(self, logname="default", seperator=";", strat_params=None):
    self.seperator = seperator
    
    self.log_placed = self.create_log_file("PLACED", "P-log_01" )
    self.create_log_strategy_parameters("PLACED", "P-log_01", params_list=strat_params)
    
    return

  def create_log_file(self, log_path, logname, strat_params=None):
    # Read CSV header string
    with open(f"{log_path}\csv_header.txt","r") as f:
      log_header = f.read()
      f.close()

    # Build time-stamped log filename
    log_filename = f"{log_path}\{logname}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"      
    
    # Create log file and insert header line (semi-colon value seperator from self.seperator)
    try:
      log_file = open(f"{log_filename}","w")
      log_file.write(f"{log_header}\n")
    except Exception as e:
      log_file = None
    
    return log_file

  def create_cash_log(self, log_path, logname, cash_list=None):
    if cash_list is None:
      return

    log_filename = f"{log_path}\{logname}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-cash.csv" 
    try:
      log_file = open(f"{log_filename}","w")
      log_file.write(f"index;date;cash\n")
    except Exception as e:
      log_file = None
      return
    
    for i,cash_line in enumerate(cash_list):
      log_file.write(f"{i}{self.seperator}{cash_line.get('date')}{self.seperator}{cash_line.get('cash')}\n")

    log_file.close()

  def create_log_strategy_parameters(self, log_path, logname, params_list=None):
    if params_list is not None:
      log_header = ""  
      log_values = ""    
      #print(f"DEBUG: {params_list}")
      for key_value in params_list._getitems():
        log_header += f"{key_value[0]}{self.seperator}"
        log_values += f"{key_value[1]}{self.seperator}"
    else:
      log_header = "#No parameters found...."
      log_values = "#No parameters found...."

    log_filename = f"{log_path}\{logname}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-params.csv"      
    # Create log file and insert header line (semi-colon value seperator from self.seperator)
    try:
      log_file = open(f"{log_filename}","w")
      log_file.write(f"{log_header}\n")
      log_file.write(f"{log_values}\n")
    except Exception as e:
      log_file = None

  def log_order_to_csv(self, data=None, indicators=None, max_hold_dates= None, log_type=None, order=None, order_data=None):
    # See folder's csv_header.txt for list of columns
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

      # TODO: Replace with a loop through indicators keys
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
    log_str  = f"{date_str}{sep}{log_type}{sep}{symbol_str}{sep}{open_str}{sep}{high_str}{sep}{low_str}{sep}{close_str}{sep}{volume_str}{sep}"
    log_str += f"{order_ref_str}{sep}{order_name_str}{sep}{order_type_str}{sep}{order_status_str}{sep}{order_price_str}{sep}{order_size_str}{sep}{order_value_str}{sep}{order_comm_str}{sep}{max_hold_date_str}{sep}"
    log_str += f"{EMA200_str}{sep}{EMA20_str}{sep}{ATR_str}{sep}{supertrend_str}{sep}{order_trade_id_str}{sep}\n"
    self.log_order.write(log_str)


  def log_trade_to_csv(self, trade=None):
    # See folder's csv_header.txt for list of columns
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

    self.log_trade.write(log_str)

  ###########################################################
  # Helper functions for PLACED ORDERS csv logger           #
  ###########################################################
  def extract_order_details(self, order):
    order_data = order.executed if order.status in [order.Completed, order.Partial, order.Cancelled, order.Expired] else order.created
    return order_data
  
  def return_order_as_csv_string(self, order):
    sep = self.seperator
    #dt = symbol_data.datetime.date(0)
    
    order_str  = f""
    order_str += f"{order.ref}{sep}"
    order_str += f"{order.getordername()}{sep}"
    order_str += f"{order.ordtypename()}{sep}"
    order_str += f"{order.getstatusname()}{sep}"

    #order_data = order.executed if order.status in [order.Completed, order.Partial, order.Cancelled, order.Expired] else order.created
    order_data = self.extract_order_details(order)
    buy_dt = bt.num2date(order_data.dt).date()
    order_str += f"{buy_dt.isoformat()}{sep}"
    order_str += f"{order_data.size}{sep}"
    order_str += f"{order_data.price}{sep}"
    order_str += f"{order_data.value}{sep}"
    order_str += f"{order_data.comm}{sep}"
    order_str += f"{order_data.pnl}{sep}"
    order_str += f"{order_data.psize}{sep}"
    order_str += f"{order_data.pprice}{sep}"    

    # print(f"DEBUG ORDER_DATA ->\nStatus:{order.status}\ndata:{order_data}") 
    # print(f"--------------------------------------")
    # print(f"Order.Completed :{order.Completed}")
    # print(f"Order.Partial   :{order.Partial}")
    # print(f"Order.Submitted :{order.Submitted}")
    # print(f"Order.Accepted  :{order.Accepted}")
    # print(f"Order.Rejected  :{order.Rejected}")
    # print(f"Order.Margin    :{order.Margin}")
    # print(f"Order.Cancelled :{order.Cancelled }")
    # print(f"Order.Canceled  :{order.Canceled}")
    # print(f"Order.Expired   :{order.Expired}")
    # print(f"--------------------------------------\n")
    # print(f"DEBUG ORDER_DATA (Dir)\n{dir(order_data)}")
    return order_str

  def return_signal_data_as_csv_str(self, signal_data):
    sep = self.seperator
    signal_str  = f""
    signal_str += f"{signal_data.get('signal_dt')}{sep}"
    signal_str += f"{signal_data.get('buy_price')}{sep}"
    signal_str += f"{signal_data.get('stop_loss')}{sep}"
    signal_str += f"{signal_data.get('take_profit')}{sep}"
    signal_str += f"{signal_data.get('max_hold_dt')}{sep}"
    signal_str += f"{signal_data.get('open')}{sep}"
    signal_str += f"{signal_data.get('high')}{sep}"
    signal_str += f"{signal_data.get('low')}{sep}"
    signal_str += f"{signal_data.get('close')}{sep}"
    signal_str += f"{signal_data.get('volume')}{sep}"

    return signal_str

  def return_trade_dollars(self, order=None, cash_data=None):
   
    if order is not None:
      order_details = self.extract_order_details(order)
      trade_date  = bt.num2date(order_details.dt).date()
      trade_value = order_details.size * order_details.price if order.getstatusname() == 'Completed' else 0
      trade_comm  = order_details.comm  if order.getstatusname() == 'Completed' else 0
      trade_pnl   = order_details.pnl   if order.getstatusname() == 'Completed' else 0
      try:
        cash_index  = [i for i,cash_line in enumerate(cash_data) if cash_line.get('date') == trade_date][0]
        trade_cash  = cash_data[cash_index].get('cash')
      except Exception as e:
        print("Error: {e}")
        trade_cash = -1
      try:
        cash_index  = [i for i,cash_line in enumerate(cash_data) if cash_line.get('date') == trade_date][0]
        trade_cash_next_day  = cash_data[cash_index+1].get('cash')
      except Exception as e:
        print("Error: {e}")
        trade_cash_next_day = 0
      
    else:
      trade_cash  = 0
      trade_cash_next_day = 0
      trade_date  = None
      trade_value = 0
      trade_comm  = 0
      trade_pnl   = 0
    
    return trade_date, trade_cash, trade_cash_next_day, trade_value, trade_comm, trade_pnl

  def log_placed_order(self, strat_trades=None, daily_cash=None):
    if strat_trades is None:
      return

    sep = self.seperator

    for trade in strat_trades:
      placed_trade_id = trade["id"]
      symbol          = trade["symbol"]
      signal_data     = trade['signal']
      buy_order       = trade['market_buy']
      stop_order      = trade['stop_limit']
      target_order    = trade['take_profit']
      if "close_position" in trade:
        close_order = trade["close_position"]
      else:
        close_order = None

      # Summary data
      trade_buy_dt, trade_buy_cash, _, trade_buy_value, trade_buy_comm, trade_buy_pnl = self.return_trade_dollars(buy_order, daily_cash)
      # Get cash value for trade_buy_date

      trade_stop_dt, trade_stop_cash, trade_stop_cash_next_day, trade_stop_value, trade_stop_comm, trade_stop_pnl = self.return_trade_dollars(stop_order, daily_cash)
      trade_target_dt, trade_target_cash, trade_target_cash_next_day, trade_target_value, trade_target_comm, trade_target_pnl = self.return_trade_dollars(target_order, daily_cash)
      trade_close_dt, trade_close_cash, trade_close_cash_next_day, trade_close_value, trade_close_comm, trade_close_pnl = self.return_trade_dollars(close_order, daily_cash)

      
      trade_sell_type = f"{'Stop'*bool(trade_stop_value)}{'Target'*bool(trade_target_value)}{'Close'*bool(trade_close_value)}"
      if trade_sell_type == 'Stop':
        trade_sell_dt = trade_stop_dt
        trade_sell_cash = trade_stop_cash
        trade_sell_cash_next_day = trade_stop_cash_next_day
      elif trade_sell_type == 'Target':
        trade_sell_dt = trade_target_dt
        trade_sell_cash = trade_target_cash
        trade_sell_cash_next_day = trade_target_cash_next_day
      elif trade_sell_type == 'Close':
        trade_sell_dt = trade_close_dt
        trade_sell_cash = trade_close_cash
        trade_sell_cash_next_day = trade_close_cash_next_day
      else:
        trade_sell_dt = None
        trade_sell_cash = 0
        trade_sell_cash_next_day = 0

      trade_sell_value = (trade_stop_value + trade_target_value + trade_close_value) * -1
      trade_sell_comm  = (trade_stop_comm  + trade_target_comm  + trade_close_comm)
      trade_sell_pnl   = (trade_stop_pnl   + trade_target_pnl   + trade_close_pnl)
      
      trade_roi_raw  = trade_sell_value - trade_buy_value
      trade_net_comm = trade_sell_comm  + trade_buy_comm
      trade_roi_net  = trade_roi_raw - trade_net_comm

      # Build csv_log line using (Strategy's signal data), Bracket_Orders (Buy dat, stop_loss data, take_profit data) and Close Position data when it exists
      log_str  = f"{placed_trade_id}{sep}{symbol}{sep}{trade_buy_cash}{sep}{trade_sell_cash}{sep}{trade_sell_cash_next_day}{sep}"
      log_str += f"{trade_buy_dt}{sep}{trade_buy_value}{sep}{trade_buy_comm}{sep}{trade_buy_pnl}{sep}"
      log_str += f"{trade_sell_dt}{sep}{trade_sell_type}{sep}{trade_sell_value}{sep}{trade_sell_comm}{sep}{trade_sell_pnl}{sep}"
      log_str += f"{trade_roi_raw}{sep}{trade_net_comm}{sep}{trade_roi_net}{sep}"
      log_str += self.return_signal_data_as_csv_str(signal_data)
      log_str += self.return_order_as_csv_string(buy_order)
      log_str += self.return_order_as_csv_string(stop_order)
      log_str += self.return_order_as_csv_string(target_order)
      if close_order is not None:
        log_str += self.return_order_as_csv_string(close_order)
      log_str += f"\n"

      # Write log line to file
      self.log_placed.write(log_str)

    
  def close(self, cash_list=None):
      self.log_placed.close()
      self.create_cash_log("PLACED", "P-Log_01", cash_list=cash_list)

