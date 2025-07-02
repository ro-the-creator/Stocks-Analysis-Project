# Imports
import yfinance as yf
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Stock Analyzer class
class StockAnalyzer:
     def __init__(self):
          ticker = input('Pick a Ticker (Do not include "$")')
          self.ticker = ticker
          self.yf = yf.Ticker(ticker)
          self.data = None
    
     def fetch_data(self, period='1mo', interval='1d'):
        stock = self.yf
        self.data = stock.history(period=period, interval=interval)
        if len(self.data) == 0:
            print("Ticker invalid. Did you exclude the dollar sign?")
        else:
            print(f"Data for ${self.ticker.upper()} received.")
            print(f"Company Name: {stock.info['shortName']}")
     
     def percent_change(self, period='2d'):
         stock = self.yf
         stock_hist = stock.history(period=period)
         df = pd.DataFrame(stock_hist)
         perc_change = ((df['Close'][-1] - df['Close'][0]) / df['Close'][0]) * 100
         print(f"Percent Change over {str(period)}: {perc_change:.2f}%")

     def detect_flagpole(self, window=5, growth_threshold=0.05):
         recent_window = self.data['Close'].iloc[-window:]
         percent_change = (recent_window.iloc[-1]-recent_window.iloc[0]) / recent_window.iloc[0]
         print(f"Flagpole change: {percent_change:.2%} over {window} days.")
         return percent_change > growth_threshold

     def pe_ratio(self):
        stock = self.yf
        dict = stock.info
        stock_trailingPE = dict.get('trailingPE')
        try:
            stock_trailingPE = float(stock_trailingPE)
        except (TypeError, ValueError):
            stock_trailingPE = "Not Available"
        print(f"Trailing PE Ratio: {stock_trailingPE:.2f}")

stock = StockAnalyzer()     
stock.fetch_data()
stock.percent_change(period='2y')
stock.percent_change(period='6mo')
stock.pe_ratio()
print("WARNING: This is not financial advice. Conduct your own research before purchasing stocks.")