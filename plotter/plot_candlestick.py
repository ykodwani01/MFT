import pandas as pd
import plotly.graph_objects as go

def plot_candlestick(data: pd.DataFrame):
    """
    Plot candlestick chart from a DataFrame with columns: 
    ['Open', 'High', 'Low', 'Close'] and optionally 'Date'.
    """

    df = data.copy()

    # Ensure datetime index
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
    else:
        df.index = pd.to_datetime(df.index)

    # Ensure columns are correctly named
    required_cols = ['Open', 'High', 'Low', 'Close']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Data must contain {required_cols} columns.")

    # Plot using Plotly
    fig = go.Figure(data=[
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close']
        )
    ])
    fig.update_layout(
        title='Candlestick Chart',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False
    )
    fig.show()
