# Stock Analysis Project

# imports
import yfinance as yf
import pandas as pd
import numpy as np

# User input & score variable
user_ticker = input('pick a ticker)')
stock_for_analysis_choice = yf.Ticker(user_ticker)
score = 0

# % change over 2yr
stock_hist_2y = stock_for_analysis_choice.history(period='2y')
df2y = pd.DataFrame(stock_hist_2y)
x2y = df2y['Close'][-1] - df2y['Close'][0]
perc_change_2y = x2y/ df2y['Close'][0] * 100

if perc_change_2y <= 10:
    score = score
if 11 <= perc_change_2y <= 20:
     score = score + 1
if 21 <= perc_change_2y <= 30:
     score = score + 2
if 31 <= perc_change_2y <= 40:
     score = score + 3
if 41 <= perc_change_2y <= 50:
     score = score + 4
if 51 <= perc_change_2y <= 60:
     score = score + 5
if 61 <= perc_change_2y <= 70:
     score = score + 6
if 71 <= perc_change_2y <= 80:
     score = score + 7
if 81 <= perc_change_2y <= 90:
     score = score + 8
if 91 <= perc_change_2y <= 100:
     score = score + 9
if 100 <= perc_change_2y:
     score = score + 10


# % change over last 6 months
stock_hist_6mo = stock_for_analysis_choice.history(period='6mo')
df6mo = pd.DataFrame(stock_hist_6mo)
x6mo = df6mo['Close'][-1] - df6mo['Close'][0]
perc_change_6mo = x6mo/ df6mo['Close'][0] * 100

if perc_change_6mo <= 10:
    score = score
if 11 <= perc_change_6mo <= 20:
     score = score + 1
if 21 <= perc_change_6mo <= 30:
     score = score + 2
if 31 <= perc_change_6mo <= 40:
     score = score + 3
if 41 <= perc_change_6mo <= 50:
     score = score + 4
if 51 <= perc_change_6mo <= 60:
     score = score + 5
if 61 <= perc_change_6mo <= 70:
     score = score + 6
if 71 <= perc_change_6mo <= 80:
     score = score + 7
if 81 <= perc_change_6mo <= 90:
     score = score + 8
if 91 <= perc_change_6mo <= 100:
     score = score + 9
if 100 <= perc_change_6mo:
     score = score + 10

# P/E ratio
dict =  stock_for_analysis_choice.info
stock_trailingPE = dict.get('trailingPE')
try:
     stock_trailingPE = float(stock_trailingPE)
     if stock_trailingPE <= 51:
          score = score
     if 46 <= stock_trailingPE <= 50:
          score = score + 1
     if 41 <= stock_trailingPE <= 45:
          score = score + 2
     if 36 <= stock_trailingPE <= 40:
          score = score + 3
     if 31 <= stock_trailingPE <= 35:
          score = score + 4
     if 26 <= stock_trailingPE <= 30:
          score = score + 5
     if 21 <= stock_trailingPE <= 25:
          score = score + 6
     if 16 <= stock_trailingPE <= 20:
          score = score + 7
     if 11 <= stock_trailingPE <= 15:
          score = score + 8
     if 6 <= stock_trailingPE <= 10:
          score = score + 9
     if 5 <= stock_trailingPE:
          score = score + 10

except (TypeError, ValueError):
     stock_trailingPE = "Not Available"
     
# Sector & Industry
sector = stock_for_analysis_choice.info.get('sector', 'N/A')
industry = stock_for_analysis_choice.info.get('industry', 'N/A')

# prints
print('Stock:', stock_for_analysis_choice.info['shortName'])
print('Sector:', sector)
print('Industry:', industry)
print('Percent Change Over 2 Years', f"{perc_change_2y:.2f}%")
print('Percent Change Over 6 Months', f"{perc_change_6mo:.2f}%")
print('P/E ratio:', stock_trailingPE)
print('-----------------------------------')
print('$',user_ticker, 'Stock Evaluation Score:', score)
print()
print('!WARNING!: This is not financial advice. Always conduct research before you purchase stocks.')


