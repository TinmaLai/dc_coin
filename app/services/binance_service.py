from binance.client import Client
from binance.exceptions import BinanceAPIException
from datetime import datetime
import pandas as pd
import pandas_ta as ta
from config import BaseConfig

class BinanceService:
    def __init__(self):
        self.client = Client(BaseConfig.BINANCE_API_KEY, BaseConfig.BINANCE_API_SECRET)
        
    def get_top_symbols(self, limit=100, quote_asset='USDT'):
        """Get top trading pairs by 24h volume"""
        try:
            tickers = self.client.get_ticker()
            df = pd.DataFrame(tickers)
            # Filter USDT pairs and sort by volume
            df = df[df['symbol'].str.endswith(quote_asset)]
            df['volume'] = df['volume'].astype(float)
            df = df.sort_values('volume', ascending=False)
            return df.head(limit)['symbol'].tolist()
        except BinanceAPIException as e:
            print(f"Error fetching top symbols: {e}")
            return []

    def get_klines(self, symbol, interval='1h', limit=100):
        """Get historical klines/candlestick data"""
        try:
            klines = self.client.get_klines(
                symbol=symbol,
                interval=interval,
                limit=limit
            )
            
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 
                'volume', 'close_time', 'quote_volume', 'trades',
                'taker_buy_base', 'taker_buy_quote', 'ignore'
            ])
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # Convert string values to float
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].astype(float)
                
            return df
            
        except BinanceAPIException as e:
            print(f"Error fetching klines for {symbol}: {e}")
            return None

    def add_technical_indicators(self, df):
        """Add technical indicators to the dataframe"""
        # Moving averages
        df['SMA_20'] = ta.sma(df['close'], length=20)
        df['SMA_50'] = ta.sma(df['close'], length=50)
        df['EMA_20'] = ta.ema(df['close'], length=20)
        
        # RSI
        df['RSI'] = ta.rsi(df['close'], length=14)
        
        # MACD
        macd = ta.macd(df['close'])
        df = pd.concat([df, macd], axis=1)
        
        # Bollinger Bands
        bollinger = ta.bbands(df['close'])
        df = pd.concat([df, bollinger], axis=1)
        
        return df

    def get_current_price(self, symbol):
        """Get current price for a symbol"""
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except BinanceAPIException as e:
            print(f"Error fetching price for {symbol}: {e}")
            return None
