from datetime import datetime, timedelta, date

class StrategyLogger():

  # TODO: Implement a log file header that is based on the indicators that were added in the strategy
  #       Loop on the keys of the indicators data


  def __init__(self, logname="default", seperator=";"):
    self.header   = "date;log_type;symbol;open;high;low;close;volume;order_ref;order_name;order_type;order_status;order_price;order_size;order_value;order_commission;max_hold_date;EMA200;EMA20;ATR;SuperTrend"

    self.filename = f"LOG_CSV\{logname}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"      
    try:
      self.log_file = open(f"{self.filename}","w")
      self.log_file.write(f"{self.header}\n")
      self.seperator = seperator
    except Exception as e:
      self.log_file = None
    return
    
  def log_to_csv(self, data=None, indicators=None, max_hold_dates= None, log_type=None, order=None, order_data=None):

    ''' Logging function to produce a CSV file for later import and analysis 
        date;log_type;symbol;open;high;low;close;volume;order_ref;order_name;order_status;order_price;order_size;order_value;order_commission;max_hold_date;EMA200;EMA20;ATR;SuperTrend
    '''
    if self.log_file is None:
      return

    symbol_data = None
    if data is not None:
      symbol_data = data
    
    if order is not None:
      symbol_data = order.data

    if symbol_data is not None:
      dt = symbol_data.datetime.date(0)
      date_str          = f"{dt.isoformat()}"
      symbol_str        = f"{symbol_data._name}"
      open_str          = f"{symbol_data.open[0]:.2f}"
      high_str          = f"{symbol_data.high[0]:.2f}"
      low_str           = f"{symbol_data.low[0]:.2f}"
      close_str         = f"{symbol_data.close[0]:.2f}"
      volume_str        = f"{symbol_data.volume[0]:.0f}"

      if max_hold_dates is not None:
        max_hold_date_str = f"{'' if max_hold_dates[symbol_data._name] == None else max_hold_dates[symbol_data._name]}"
      else:
        max_hold_date_str = ''

      # TODO: Replace wity a loop thourgh indicators keys
      EMA200_str        = f"{indicators[symbol_data]['ema2'][0]:.2f}"
      EMA20_str         = f"{indicators[symbol_data]['ema1'][0]:.2f}"
      ATR_str           = f"{indicators[symbol_data]['atr'][0]:.2f}"
      supertrend_str    = f"{indicators[symbol_data]['supertrend'][0]:.2f}"
    else:
      # Something's wrong bad data available
      return

    if log_type is not None:
      log_type   = f"{log_type}"
    else:
      log_type   = ""

    if order is not None:
      order_ref_str    = f"{order.ref}"
      order_name_str   = f"{order.getordername()}"
      order_type_str   = f"{order.ordtypename()}"
      order_status_str = f"{order.getstatusname()}"
    else:
      order_ref_str    = ""
      order_name_str   = ""
      order_type_str   = ""
      order_status_str = ""

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
    log_str += f"{EMA200_str}{sep}{EMA20_str}{sep}{ATR_str}{sep}{supertrend_str}{sep}\n"
    self.log_file.write(log_str)

  def close(self):
      self.log_file.close()