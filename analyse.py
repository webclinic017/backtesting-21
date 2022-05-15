import os


import os
import pandas as pd

from pathlib import Path

def get_latest_log_filename(base_dir):
  basepath = Path(f"{base_dir}/")
  # extract the file with the highest mtime (modified date/time)
  _timestamp, file_name = max((f.stat().st_mtime, f) for f in basepath.iterdir() if f.is_file())
  return file_name

def load_latest_log(base_dir):
  latest_log_file = get_latest_log_filename(base_dir)
  log_df = pd.read_csv(latest_log_file, sep=";", index_col=False).set_index("date")
  return log_df

def merge_trades(trades_df):
  print(trades_df)
  merged_trades = trades_df.groupby([trades_df.ref])
  print(merged_trades.index.names)
  #for trade in trades_df.groupby([trades_df.ref]):
  #  print(trade)

def main():
  #orders_log = latest_log("LOG_CSV")
  #orders_df = pd.read_csv(orders_log, sep=";")
  orders_df = load_latest_log("LOG_CSV")
  print(orders_df.columns)
  
  #trades_log = latest_log("TRADES")
  #trades_df = pd.read_csv(trades_log, sep=";")
  trades_df = load_latest_log("TRADES")
  print(trades_df.columns)

  #merge_trades(trades_df)


if __name__ == "__main__":
  main()
