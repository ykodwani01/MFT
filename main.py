import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import requests
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from dotenv import load_dotenv
import os
from pattern.spinningTop import detect_all_spinning
from pattern.shootingStars import *
from pattern.engulfing import detect_all_engulfing
from plotter.plot_candlestick import plot_candlestick
import yaml
from pnl.findTrades import calculate_profit_loss


from config.config import Config
from data.fetcher import Fetcher
from pattern.marubozu import Marubozu
load_dotenv()

config=Config()
fetcher = Fetcher()

stock_names = config.get_stocks()

# Fetch daily OHLC data for each stock and detect spinning tops
res = 0
for symbol in stock_names:
    print(f"Fetching data for {symbol}")
    data = fetcher.fetch_daily_ohlc(symbol)
    print(data)
    
    marubozu = Marubozu(data)
    marubozu_df = marubozu.detect_all_marubozus(
        upper_wick_threshold=0.5,
        lower_wick_threshold=0.5,
        min_candle_length=1.0,
        max_candle_length=10.0
    )
    
    # spinning_df = detect_all_spinning(
    #     data,
    # )

    # shooting_df = detect_all_shooting_stars(
    #     data,
    #     # upper_wick_threshold=0.5,
    #     # lower_wick_threshold=0.5,
    #     # min_candle_length=1.0,
    #     # max_candle_length=10.0

    # )

    # englufing_df = detect_all_engulfing(
    #     data
    # )

    # print(f"Detected  Candles for {symbol}:")
    # # print(spinning_df)

    #Marubozu
    total_profit_loss,trades = calculate_profit_loss(data, marubozu_df, lookback=8, take_profit_pct=0.07, stop_pct=0.035,trade_type="reversal")
    print(f"Total Profit/Loss: {total_profit_loss}")
    for trade in trades:
        print(f"Buy on {trade['entry_date']} at {trade['entry_price']}, Sell on {trade['exit_date']} at {trade['exit_price']}, Shooting Profit/Loss: {trade['pnl']}")
    res += total_profit_loss

    
    # # SHOOTING STAR PATTERN
    # total_profit_loss,trades = calculate_profit_loss(data, shooting_df, lookback=8, take_profit_pct=0.07, stop_pct=0.035,type="reversal")
    # print(f"Total Profit/Loss: {total_profit_loss}")
    # for trade in trades:
    #     print(f"Buy on {trade['entry_date']} at {trade['entry_price']}, Sell on {trade['exit_date']} at {trade['exit_price']}, Shooting Profit/Loss: {trade['pnl']}")
    # res += total_profit_loss

    # # DOJI PATTERN
    # total_profit_loss, trades = calculate_profit_loss(data, spinning_df, lookback=5, take_profit_pct=0.07, stop_pct=0.04,type="reversal")
    # print(f"Total Profit/Loss: {total_profit_loss}")
    # for trade in trades:
    #     print(f"Buy on {trade['entry_date']} at {trade['entry_price']}, Sell on {trade['exit_date']} at {trade['exit_price']}, Spinning Profit/Loss: {trade['pnl']}")
    # res += total_profit_loss

    # #ENGULFING PATTERN
    # print("Engulfing Patterns")
    # print(englufing_df)
    # total_profit_loss, trades = calculate_profit_loss(data, englufing_df, lookback=5, take_profit_pct=0.07, stop_pct=0.04,type="reversal")
    # print(f"Total Profit/Loss: {total_profit_loss}")
    # for trade in trades:
    #     print(f"Buy on {trade['entry_date']} at {trade['entry_price']}, Sell on {trade['exit_date']} at {trade['exit_price']}, Engulfing Profit/Loss: {trade['pnl']}")
    # res += total_profit_loss

print("Net from all stocks" ,res)