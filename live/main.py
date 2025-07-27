import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from live.signals import get_signal
from live.trading import place_order
from data.fetcher import Fetcher
from config.config import Config

def main():
    config = Config()
    fetcher = Fetcher()
    stock_names = config.get_stocks()

    for symbol in stock_names:
        print(f"Getting signal for {symbol}")
        signal = get_signal(symbol)

        if signal:
            print(f"Signal for {symbol}: {signal}")
            data = fetcher.fetch_data(symbol, period="1d")
            if not data.empty:
                price = data.iloc[-1]['Close']
                target_price = price * 1.03 if signal['signal'] == 'bullish' else price * 0.97
                place_order(symbol, signal, price, target_price)

if __name__ == "__main__":
    main()
