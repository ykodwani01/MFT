import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import requests
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from dotenv import load_dotenv
import os
from data.fetcher import fetch_daily_ohlc
from pattern.spinningTop import detect_all_spinning
from plotter.plot_candlestick import plot_candlestick
import yaml
from pnl.findTrades import calculate_profit_loss

CONFIG_PATH =  './config/service.yaml'

load_dotenv()

#Load configuration from YAML file
with open(CONFIG_PATH, 'r') as file:
    config = yaml.safe_load(file)

stock_names = config.get('stocks')
print(stock_names)


# Fetch daily OHLC data for each stock and detect spinning tops
res = 0
for symbol in stock_names:
    data = fetch_daily_ohlc(symbol)
    spinning_df = detect_all_spinning(
        data,
        upper_wick_threshold=0.5,
        lower_wick_threshold=0.5,
        min_candle_length=1.0,
        max_candle_length=10.0
    )

    print(f"Detected Spinning Candles for {symbol}:")
    print(spinning_df)

    # plot_candlestick(data)

    total_profit_loss, trades = calculate_profit_loss(data, spinning_df, lookback=5, take_profit_pct=0.07, stop_pct=0.04,type="reversal")
    res += total_profit_loss
    print(f"Total Profit/Loss: {total_profit_loss}")
    for trade in trades:
        print(f"Buy on {trade['entry_date']} at {trade['entry_price']}, Sell on {trade['exit_date']} at {trade['exit_price']}, Profit/Loss: {trade['pnl']}")

print("Net from all stocks" ,res)