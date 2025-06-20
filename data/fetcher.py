import requests
from dotenv import load_dotenv
import os

load_dotenv()

apikey = os.getenv("ALPHA_VANTAGE_API_KEY")

def fetch_daily_ohlc(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={apikey}"
    r = requests.get(url)
    return r.json()