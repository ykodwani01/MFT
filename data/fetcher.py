import requests
from dotenv import load_dotenv
import os
import yfinance as yf
class Fetcher:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        if not self.api_key:
            raise ValueError("API key not found. Please set ALPHA_VANTAGE_API_KEY in your environment variables.")
        self.base_url = "https://www.alphavantage.co/query"
    
    def fetch_daily_ohlc(self, symbol):
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'apikey': self.api_key,
            'datatype': 'json'
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching data for {symbol}: {response.status_code} - {response.text}")
        
        data = response.json().get('Time Series (Daily)', {})
        
        return data
    
    def fetch_data(self, symbol): 
        df = yf.download(symbol, period="6mo", interval="1d")
        df.columns.name = None
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]  # Flatten columns
        df.reset_index(inplace=True)
        return df
