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
         self.period = period
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
            return stock_trailingPE
         except (TypeError, ValueError):
            return 0

     def volume_check(self, type='volume'):
         volume_type = self.info.get(type)
         return volume_type

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
     def score(self):

        # pe ratio score
         pe_ratio = self.pe_ratio()
         scorechart_pe = {'score': list(range(1,11))}
         scpe = pd.DataFrame(scorechart_pe)
         results_pe = []

         if pe_ratio >= 52:
            results_pe.append(True)
         else:
            results_pe.append(False)
         for x in range(0,8):
            higher_pe = 51-x*5
            lower_pe = higher_pe - 5
            if lower_pe <= pe_ratio <= higher_pe:
               results_pe.append(True)
            else:
               results_pe.append(False)
         if pe_ratio <= 0.9:
            results_pe.append(True)
         else:
            results_pe.append(False)

         scpe['true_false'] = results_pe
         scpe_true = scpe[scpe['true_false']==True]['score'].iloc[0]


        # percent change 2y score
         percent_2y = self.percent_change(period='2y')
         scorechart_2y6mo = {'score': list(range(10,0, -1))}
         sc2y6mo = pd.DataFrame(scorechart_2y6mo)
         results_2y = []

         if percent_2y >= 102:
            results_2y.append(True)
         else:
            results_2y.append(False)
         for y in range(0,8):
            higher_2y6mo = 101 - y*12
            lower_2y6mo = higher_2y6mo - 10
            if lower_2y6mo <= percent_2y <= higher_2y6mo:
                results_2y.append(True)
            else:
                results_2y.append(False)
         if percent_2y <= 1:
            results_2y.append(True)
         else:
            results_2y.append(False)

         sc2y6mo['2y'] = results_2y
         sc2y_true = sc2y6mo[sc2y6mo['2y']==True]['score'].iloc[0]


         # percent change 6mo score
         percent_6mo = self.percent_change(period='6mo')
         results_6mo = []

         if percent_6mo >= 102:
            results_6mo.append(True)
         else:
            results_6mo.append(False)
         for y in range(0,8):
            higher_2y6mo = 101 - y*10
            lower_2y6mo = higher_2y6mo - 10
            if lower_2y6mo <= percent_6mo <= higher_2y6mo:
                results_6mo.append(True)
            else:
                results_6mo.append(False)
         if percent_6mo <= 1:
            results_6mo.append(True)
         else:
            results_6mo.append(False)

         sc2y6mo['6mo'] = results_6mo
         sc6mo_true = sc2y6mo[sc2y6mo['6mo']==True]['score'].iloc[0]


         # percent change 2d score
         percent_2d = self.percent_change(period='2d')
         scorechart_2d = {'score': list(range(10,0, -1))}
         sc2d = pd.DataFrame(scorechart_2d)
         results_2d = []

         if percent_2d >= 21:
            results_2d.append(True)
         else:
            results_2d.append(False)
         for z in range(0,8):
            higher_2d = 21-z*2.5
            lower_2d = higher_2d - 2
            if lower_2d <= percent_2d <= higher_2d:
               results_2d.append(True)
            else:
               results_2d.append(False)
         if percent_2d <= 2:
            results_2d.append(True)
         else:
            results_2d.append(False)

         sc2d['true_false'] = results_2d
         sc2d_true = sc2d[sc2d['true_false']==True]['score'].iloc[0]


         # volume change check

         volume = self.volume_check(type='volume')
         avg_volume = self.volume_check(type='averageVolume')
         volume_change = ((volume - avg_volume)/avg_volume)*100
         results_volume = []

         if volume_change >= 21:
            results_volume.append(True)
         else:
            results_volume.append(False)
         for d in range(0,8):
            higher_vol = 21-d*2.5
            lower_vol = higher_vol-2
            if lower_vol <= volume_change <= higher_vol:
               results_volume.append(True)
            else:
               results_volume.append(False)
         if volume_change <= 2:
               results_volume.append(True)
         else:
               results_volume.append(False)

         sc2d['volume_truefalse'] = results_volume
         sc2d_vol_true = sc2d[sc2d['volume_truefalse']==True]['score'].iloc[0]

         final_score = scpe_true + sc2y_true + sc6mo_true + sc2d_true + sc2d_vol_true
         print(f'Score: {final_score}/50')            



# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

     def run_all(self, pole_window=5, pole_threshold=0.05, flag_window=7, flag_threshold=0.01):
         self.fetch_data()
         print('----------------------------')
         print('Percent Change:')
         self.percent_change(period='2y')
         print(f"Percent Change over {str(self.period)}: {self.percent_change(period='2y'):.2f}%")
         self.percent_change(period='6mo')
         print(f"Percent Change over {str(self.period)}: {self.percent_change(period='6mo'):.2f}%")
         self.percent_change(period='2d')
         print(f"Percent Change over {str(self.period)}: {self.percent_change(period='2d'):.2f}%")
         print('----------------------------')
         print('P/E Ratio:')
         stock_trailingPE = self.pe_ratio()
         if stock_trailingPE != 0:
            print(f"Trailing PE Ratio: {stock_trailingPE:.2f}")
         if stock_trailingPE == 0:
            print(f"Trailing PE Ratio: Not Available")
         print('----------------------------')
         print('Bull Flag Detection:')
         self.detect_flagpole(pole_window=pole_window, flag_window=flag_window, pole_threshold=pole_threshold)
         self.detect_flag(flag_window=flag_window, flag_threshold=flag_threshold)
         self.detect_flag_pattern()
         print('----------------------------')
         print('Volume:')
         volume = self.volume_check(type='volume')
         avg_volume = self.volume_check(type='averageVolume')
         print(f'Current Stock Volume: {volume}. Average Volume: {avg_volume}')
         print(f'${self.ticker.upper()} volume change is {((volume - avg_volume)/avg_volume)*100:.2f}%.')
         if volume > (avg_volume * 1.05):
             print('Stock volume is above average volume --> High interest.')
         if (avg_volume*1.05) > volume > (avg_volume*0.95):
             print('Stock volume is near average volume --> Average interest.')
         if (avg_volume*0.95) > volume:
             print('Stock volume is below average volume --> Low general interest.')
         print('----------------------------')
         self.score()
         print("WARNING: This is not financial advice. Conduct your own research before purchasing stocks.")

stock = StockAnalyzer()
stock.run_all(pole_window=5, pole_threshold=0.05, flag_window=7, flag_threshold=0.01)