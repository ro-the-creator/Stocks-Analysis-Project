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
          self.info = self.yf.info
          self.hist = None
    
     def fetch_data(self, period='6mo', interval='1d'):
        self.hist = self.yf.history(period=period, interval=interval)
        if len(self.hist) == 0:
            print('--------------------------------------------------')
            print("Ticker invalid. Did you exclude the dollar sign?")
            print('--------------------------------------------------')
        else:
            print(f"Data for ${self.ticker.upper()} received. Contains {len(self.hist)} rows.")
            print(f"Company Name: {self.yf.info['shortName']}")
     
     def percent_change(self, period='2d'):
         stock_hist = self.yf.history(period=period)
         df = pd.DataFrame(stock_hist)
         perc_change = ((df['Close'][-1] - df['Close'][0]) / df['Close'][0]) * 100
         perc_change2y = perc_change
         print(f"Percent Change over {str(period)}: {perc_change:.2f}%")

         return perc_change

     def detect_flagpole(self, pole_window=5, flag_window=7, pole_threshold=0.05):
         recent_window = self.hist['Close'].iloc[-(pole_window + flag_window):-flag_window]
         percent_change = ((recent_window.iloc[-1]-recent_window.iloc[0]) / recent_window.iloc[0])
         percent_change100 = percent_change * 100
         print(f"Flagpole change: {percent_change100:.2f}% over {pole_window} days before flag splice.")
         self.pole_check = percent_change >= pole_threshold

     def detect_flag(self, flag_window=7, flag_threshold=0.01):
         recent_window = self.hist['Close'].iloc[-flag_window:]
         percent_change = ((recent_window.iloc[-1] - recent_window.iloc[0]) / recent_window.iloc[0])
         percent_change100 = percent_change * 100
         print(f"Flag change: {percent_change100:.2f}% over {flag_window} days after flagpole.")
         self.flag_check = percent_change <= flag_threshold

     def detect_flag_pattern(self):
         if self.pole_check == True and self.flag_check == True:
             print("Bull Flag Detected. Confirm with Volume.")
         elif self.pole_check == False or self.flag_check == False:
             print("Bull Flag not Detected.")
         else:
             print('Error')

     def pe_ratio(self):
         stock_trailingPE = self.info.get('trailingPE')
         try:
            stock_trailingPE = float(stock_trailingPE)
            print(f"Trailing PE Ratio: {stock_trailingPE:.2f}")
         except (TypeError, ValueError):
            print(f"Trailing PE Ratio: Not Available")

     def volume_check(self):
         volume = self.info.get('volume')
         avg_volume = self.info.get('averageVolume')
         print(f'Current Stock Volume: {volume}. Average Volume: {avg_volume}')
         print(f'${self.ticker.upper()} volume change is {((volume - avg_volume)/avg_volume)*100:.2f}%.')
         if volume > (avg_volume * 1.05):
             print('Stock volume is above average volume --> High interest.')
         if (avg_volume*1.05) > volume > (avg_volume*0.95):
             print('Stock volume is near average volume --> Average interest.')
         if (avg_volume*0.95) > volume:
             print('Stock volume is below average volume --> Low general interest.')

     def score(self):
         score = 0

         perc_change2y = self.percent_change(period='2y')
         if perc_change2y <= 10:
            score = score
         if 11 <= perc_change2y <= 20:
            score = score + 1
         if 21 <= perc_change2y <= 30:
            score = score + 2
         if 31 <= perc_change2y <= 40:
            score = score + 3
         if 41 <= perc_change2y <= 50:
            score = score + 4
         if 51 <= perc_change2y <= 60:
            score = score + 5
         if 61 <= perc_change2y <= 70:
            score = score + 6
         if 71 <= perc_change2y <= 80:
            score = score + 7
         if 81 <= perc_change2y <= 90:
            score = score + 8
         if 91 <= perc_change2y <= 100:
            score = score + 9
         if 100 <= perc_change2y:
            score = score + 10
         
         perc_change6mo = self.percent_change(period='6mo')
         if perc_change6mo <= 10:
            score = score
         if 11 <= perc_change6mo <= 20:
            score = score + 1
         if 21 <= perc_change6mo <= 30:
            score = score + 2
         if 31 <= perc_change6mo <= 40:
            score = score + 3
         if 41 <= perc_change6mo <= 50:
            score = score + 4
         if 51 <= perc_change6mo <= 60:
            score = score + 5
         if 61 <= perc_change6mo <= 70:
            score = score + 6
         if 71 <= perc_change6mo <= 80:
            score = score + 7
         if 81 <= perc_change6mo <= 90:
            score = score + 8
         if 91 <= perc_change6mo <= 100:
            score = score + 9
         if 100 <= perc_change6mo:
            score = score + 10
         
         perc_change2d = self.percent_change(period='2d')
         if perc_change2d <= 10:
            score = score
         if 11 <= perc_change2d <= 20:
            score = score + 1
         if 21 <= perc_change2d <= 30:
            score = score + 2
         if 31 <= perc_change2d <= 40:
            score = score + 3
         if 41 <= perc_change2d <= 50:
            score = score + 4
         if 51 <= perc_change2d <= 60:
            score = score + 5
         if 61 <= perc_change2d <= 70:
            score = score + 6
         if 71 <= perc_change2d <= 80:
            score = score + 7
         if 81 <= perc_change2d <= 90:
            score = score + 8
         if 91 <= perc_change2d <= 100:
            score = score + 9
         if 100 <= perc_change2d:
            score = score + 10

         print(perc_change2y)
         return score

     def run_all(self, pole_window=5, pole_threshold=0.05, flag_window=7, flag_threshold=0.01):
         self.fetch_data()
         print('----------------------------')
         print('Percent Change:')
         self.percent_change(period='2y')
         self.percent_change(period='6mo')
         self.percent_change(period='2d')
         print('----------------------------')
         print('P/E Ratio:')
         self.pe_ratio()
         print('----------------------------')
         print('Bull Flag Detection:')
         self.detect_flagpole(pole_window=pole_window, flag_window=flag_window, pole_threshold=pole_threshold)
         self.detect_flag(flag_window=flag_window, flag_threshold=flag_threshold)
         self.detect_flag_pattern()
         print('----------------------------')
         print('Volume:')
         self.volume_check()
         print('----------------------------')
         print(f'Score: {self.score()}/100')
         print("WARNING: This is not financial advice. Conduct your own research before purchasing stocks.")

stock = StockAnalyzer()
stock.run_all(pole_window=5, pole_threshold=0.05, flag_window=7, flag_threshold=0.01)