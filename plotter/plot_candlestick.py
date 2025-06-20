import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
def plot_candlestick(data):
    # Extract the time series data and convert it into a DataFrame
    time_series = data.get("Time Series (Daily)", {})

    # Convert the time series into a DataFrame
    df = pd.DataFrame.from_dict(time_series, orient='index')

    # Convert all values to float and rename columns for mplfinance compatibility
    df = df[['1. open', '2. high', '3. low', '4. close', '5. volume']].astype(float)
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

    # Convert the index to datetime
    df.index = pd.to_datetime(df.index)
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

    fig.show()
