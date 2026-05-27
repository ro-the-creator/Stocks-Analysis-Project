# Imports

import yfinance as yf
import pandas as pd
import numpy as np
import argparse
import json
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Stock Analyzer class

class StockAnalyzer:
     def __init__(self, ticker):
          self.ticker = ticker
          self.yf = yf.Ticker(ticker)
          self.info = self.yf.info
          self.hist = None
    
     def fetch_data(self, period='6mo', interval='1d'):
        self.hist = self.yf.history(period=period, interval=interval)
        return self.hist
     
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
         self.pole_check = percent_change >= pole_threshold
         return percent_change100

     def detect_flag(self, flag_window=7, flag_threshold=0.01):
         recent_window = self.hist['Close'].iloc[-flag_window:]
         percent_change = ((recent_window.iloc[-1] - recent_window.iloc[0]) / recent_window.iloc[0])
         percent_change100 = percent_change * 100
         self.flag_check = percent_change <= flag_threshold
         return percent_change100

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
         scorechart_pe = {'score': list(range(1,21,2))}
         scpe = pd.DataFrame(scorechart_pe)
         results_pe = []

         if pe_ratio > 51:
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
         if pe_ratio < 11:
            results_pe.append(True)
         else:
            results_pe.append(False)

         scpe['true_false'] = results_pe
         scpe_true = scpe[scpe['true_false']==True]['score'].iloc[0]


        # percent change 2y score
         percent_2y = self.percent_change(period='2y')
         scorechart_2y6mo = {'score': list(range(20,0, -2))}
         sc2y6mo = pd.DataFrame(scorechart_2y6mo)
         results_2y = []

         if percent_2y > 101:
            results_2y.append(True)
         else:
            results_2y.append(False)
         for y in range(0,8):
            higher_2y6mo = 101 - y*10
            lower_2y6mo = higher_2y6mo - 10
            if lower_2y6mo <= percent_2y <= higher_2y6mo:
                results_2y.append(True)
            else:
                results_2y.append(False)
         if percent_2y < 21:
            results_2y.append(True)
         else:
            results_2y.append(False)

         sc2y6mo['2y'] = results_2y
         sc2y_true = sc2y6mo[sc2y6mo['2y']==True]['score'].iloc[0]


         # percent change 6mo score
         percent_6mo = self.percent_change(period='6mo')
         results_6mo = []

         if percent_6mo > 101:
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
         if percent_6mo < 21:
            results_6mo.append(True)
         else:
            results_6mo.append(False)

         sc2y6mo['6mo'] = results_6mo
         sc6mo_true = sc2y6mo[sc2y6mo['6mo']==True]['score'].iloc[0]


         # percent change 2d score
         percent_2d = self.percent_change(period='2d')
         scorechart_2d = {'score': list(range(20,0, -2))}
         sc2d = pd.DataFrame(scorechart_2d)
         results_2d = []

         if percent_2d > 3:
            results_2d.append(True)
         else:
            results_2d.append(False)
         for z in range(0,8):
            higher_2d = 3-z*0.3
            lower_2d = higher_2d - 0.3
            if lower_2d <= percent_2d <= higher_2d:
               results_2d.append(True)
            else:
               results_2d.append(False)
         if percent_2d < 0.3:
            results_2d.append(True)
         else:
            results_2d.append(False)

         sc2d['true_false'] = results_2d
         sc2d_true = sc2d[sc2d['true_false']==True]['score'].iloc[0]


         # volume change score

         volume = self.volume_check(type='volume')
         avg_volume = self.volume_check(type='averageVolume')
         volume_change = ((volume - avg_volume)/avg_volume)*100
         results_volume = []

         if volume_change > 21:
            results_volume.append(True)
         else:
            results_volume.append(False)
         for d in range(0,8):
            higher_vol = 21-d*2.5
            lower_vol = higher_vol-2.5
            if lower_vol <= volume_change <= higher_vol:
               results_volume.append(True)
            else:
               results_volume.append(False)
         if volume_change < 1:
               results_volume.append(True)
         else:
               results_volume.append(False)

         sc2d['volume_truefalse'] = results_volume
         sc2d_vol_true = sc2d[sc2d['volume_truefalse']==True]['score'].iloc[0]

         final_score = scpe_true + sc2y_true + sc6mo_true + sc2d_true + sc2d_vol_true
         return final_score            



# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

     def report_it(self):
        report = {}
        self.fetch_data()
        if len(self.hist) == 0:
            report['fetch_data'] = "Ticker invalid. Did you exclude the dollar sign?"
        else:
            report['fetch_data'] = f"Data for ${self.ticker.upper()} received. Contains {len(self.hist)} rows." 
            report['company_name'] = self.yf.info['shortName']
            report['2y_change'] = round(float(self.percent_change(period='2y')),2)
            report['6mo_change'] = round(float(self.percent_change(period='6mo')),2)
            report['2d_change'] = round(float(self.percent_change(period='2d')),2)
        
            stock_trailingPE = self.pe_ratio()
            if stock_trailingPE != 0:
               report['trailing_pe'] = stock_trailingPE
            if stock_trailingPE == 0:
               report['trailing_pe'] = "Not Available"

            report['flagpole_change'] = f"{self.detect_flagpole(pole_window=5, flag_window=7, pole_threshold=0.05):.2f}% over 5 days before flag splice."
            report['flag_change'] = f"{self.detect_flag(flag_window=7, flag_threshold=0.01):.2f}% over 2 days after flagpole."
            if self.pole_check == True and self.flag_check == True:
               report['bull_flag_detector'] = "Bull Flag Detected. Confirm with Volume."
            elif self.pole_check == False or self.flag_check == False:
               report['bull_flag_detector'] = "Bull Flag not Detected."
            else:
               report['bull_flag_detector'] = 'Error'

            volume = self.volume_check(type='volume')
            avg_volume = self.volume_check(type='averageVolume')
            report['volume'] = volume
            report['avg_volume'] = avg_volume
            report['volume_difference'] = f"{((volume - avg_volume)/avg_volume)*100:.2f}%"
            if volume > (avg_volume * 1.05):
               report['volume_check'] = 'Stock volume is above average volume --> High interest.'
            if (avg_volume*1.05) > volume > (avg_volume*0.95):
               report['volume_check'] = 'Stock volume is near average volume --> Average interest.'
            if (avg_volume*0.95) > volume:
               report['volume_check'] = 'Stock volume is below average volume --> Low general interest.'
            else:
               report['volume_check'] = 'Error'

            report['final_score'] = f'Score: {self.score()}/100'
            report['warning'] = "WARNING: This is not financial advice. Conduct your own research before purchasing stocks."
        return report




# Stock Analyzer argument is the stock ticker, will take input from frontend to receive a report in list format

# stock = StockAnalyzer(STOCK TICKER)
# stock_report = stock.report_it()



# Or converted to DataFrame

# stock_df = pd.DataFrame(stock_report, index=[0])


def _to_json_safe(value):
   if isinstance(value, (np.integer, np.floating)):
      return value.item()
   if pd.isna(value):
      return None
   return value


def run_cli():
   parser = argparse.ArgumentParser(description="Run stock analysis and output JSON report.")
   parser.add_argument("ticker", help="Ticker symbol (e.g. AAPL)")
   args = parser.parse_args()

   try:
      analyzer = StockAnalyzer(args.ticker)
      report = analyzer.report_it()
      normalized_report = {k: _to_json_safe(v) for k, v in report.items()}
      print(json.dumps(normalized_report, default=_to_json_safe))
   except Exception as exc:
      print(json.dumps({"error": str(exc)}))


if __name__ == "__main__":
   run_cli()
