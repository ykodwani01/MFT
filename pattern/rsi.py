import pandas as pd

class RSI:
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with a DataFrame (e.g. from yfinance) having
        columns: ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'].
        """
        self.data = data.copy()
        # Ensure 'Date' is a column, not just an index
        if 'Date' not in self.data.columns and isinstance(self.data.index, pd.DatetimeIndex):
            self.data = self.data.reset_index().rename(columns={'index': 'Date'})

    def calculate_rsi(self, window: int = 14) -> pd.DataFrame:
        """
        Calculate RSI and type, returning a DataFrame with columns:
          ['date','type','open','high','low','close','volume','rsi','type'].

        - 'type': same as 'type' (bullish/bearish/None)
        - 'type': 'bullish' if RSI < 30, 'bearish' if RSI > 75, else None
        """
        df = self.data.copy()

        # 1. Compute RSI
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window=window).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=window).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))

        # 2. Generate type
        df['type'] = df['rsi'].apply(
            lambda x: 'bullish' if x < 25 else ('bearish' if x > 75 else None)
        )
        # Remove rows where 'type' is None
        df = df[df['type'].notnull()]

        out = df.rename(columns={
            'Date': 'date',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        })[['date','type','open','high','low','close','volume','rsi']]

        # 4. Drop rows until RSI is first valid
        return out.dropna(subset=['rsi']).reset_index(drop=True)
