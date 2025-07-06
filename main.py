import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import requests
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from dotenv import load_dotenv
import os
from pattern.shootingStars import *
# from pattern.engulfing import detect_all_engulfing
from pattern.shootingStars import ShootingStar
from plotter.plot_candlestick import plot_candlestick
import yaml
from pattern.engulfing import EngulfingPattern
from pnl.findTrades import calculate_profit_loss
import yfinance as yf

from config.config import Config
from data.fetcher import Fetcher
from pattern.marubozu import Marubozu
from pattern.spinningTop import SpinningTop
load_dotenv()

config=Config()
fetcher = Fetcher()

stock_names = config.get_stocks()

# Fetch daily OHLC data for each stock and detect spinning tops
res1 = 0
res2 = 0
res3 = 0
res4 = 0
for symbol in stock_names:
    print(f"Fetching data for {symbol}")
    data = fetcher.fetch_data(symbol)
    # print(data)
    
    marubozu = Marubozu(data)
    marubozu_df = marubozu.detect_all_marubozus(
        upper_wick_threshold=0.5,
        lower_wick_threshold=0.5,
        min_candle_length=1.0,
        max_candle_length=10.0
    )
    
    spinning = SpinningTop(data)
    spinning_df = spinning.detect_spinning_tops()

    shooting = ShootingStar(data)
    shooting_df = shooting.detect_shooting_stars()

    engulfig = EngulfingPattern(data)
    englufing_df = engulfig.detect_engulfing_patterns()
    # englufing_df = detect_all_engulfing(
    #     data
    # )

    # print(f"Detected  Candles for {symbol}:")
    # # print(spinning_df)
    # plot_candlestick(data)
    #Marubozu
    print(f"Marubozu Patterns for {symbol}:")
    print(marubozu_df)
    total_profit_loss,trades = calculate_profit_loss(data, marubozu_df, take_profit_pct=0.045, stop_pct=0.02)
    print(f"Total Profit/Loss: {total_profit_loss}")
    for trade in trades:
        print(f"Buy on {trade['entry_date']} at {trade['entry_price']}, Sell on {trade['exit_date']} at {trade['exit_price']}, marubozu Profit/Loss: {trade['pnl']}")
    res1 += total_profit_loss

    
    # SHOOTING STAR PATTERN
    total_profit_loss,trades = calculate_profit_loss(data, shooting_df, take_profit_pct=0.06, stop_pct=0.03)
    print(f"Total Profit/Loss: {total_profit_loss}")
    for trade in trades:
        print(f"Buy on {trade['entry_date']} at {trade['entry_price']}, Sell on {trade['exit_date']} at {trade['exit_price']}, Shooting Profit/Loss: {trade['pnl']}")
    res3 += total_profit_loss

    # DOJI PATTERN
    print(spinning_df)
    total_profit_loss, trades = calculate_profit_loss(data, spinning_df, take_profit_pct=0.07, stop_pct=0.04)
    print(f"Total Profit/Loss: {total_profit_loss}")
    for trade in trades:
        print(f"Buy on {trade['entry_date']} at {trade['entry_price']}, Sell on {trade['exit_date']} at {trade['exit_price']}, Spinning Profit/Loss: {trade['pnl']}")
    res2 += total_profit_loss

    #ENGULFING PATTERN
    print("Engulfing Patterns")
    print(englufing_df)
    total_profit_loss, trades = calculate_profit_loss(data, englufing_df, take_profit_pct=0.08, stop_pct=0.03)
    print(f"Total Profit/Loss: {total_profit_loss}")
    for trade in trades:
        print(f"Buy on {trade['entry_date']} at {trade['entry_price']}, Sell on {trade['exit_date']} at {trade['exit_price']}, Engulfing Profit/Loss: {trade['pnl']}")
    res4 += total_profit_loss

print("Net from all stocks" ,res1,res2,res3,res4)