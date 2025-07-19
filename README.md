# Stock Analysis Project
<p align='center'>
This is a project using the yfinance API to access Yahoo Finance's publicly available financial and market data. Several functions within scripts will run an analysis on any given stock and give it a scored valuation that will help you determine whether the stock is worth buying.
</p>

![](https://miro.medium.com/v2/resize:fit:1400/1*_12VG957NJA854PvZFJNDA.png)

## Overview

- Created by Rolando Mancilla-Rojas
   * My [GitHub](https://github.com/ro-the-creator)
   * My [LinkedIn](https://www.linkedin.com/in/rolandoma33/)

- Project started June 9, 2025 | **WORK IN PROGRESS**

## Sources
- [yfinance](https://github.com/ranaroussi/yfinance)
  - GitHub repository to ranaroussi's yfinance API

- [Yahoo Finance](https://finance.yahoo.com/)
  - Data scraped from API

- [w3 Resources](https://www.w3resource.com/index.php)
  - Tons of help from back-end tutorials

## Changelog

### June
- 6/9/2025 8:00pm :
  - Created repo, installed yfinance

- 6/10/2025 4:15pm :
  - Added 2year stock percentage change
  - Created a scoring system

- 6/11/2025 3:57pm :
  - Added 6mo stock percentage change + scoring system
  - Created Stock-Analysis-Project.py

- 6/12/2025 3:22pm :
  - Added trailing PE ratio + scoring system
  - Updated Stock-Analysis-Project.py
  - Added stock_info_csvs folder to import .csv's of stock info

### July
- 7/1/2025 5:28pm :
  - Simplified PE ratio code lines
  - used `try:` statements to account for errors

- 7/2/2025 7:46pm :
  - added new files implementing class `StockAnalyzer:`
  - simplified analytical functions into methods.

- 7/3/2025 5:13pm :
  - converted old procedural code into classes
  - added bull flag detection

- 7/7/2025 6:06pm :
  - added Volume/Avg Volume calculations
  - cleaned up run_all() method

- 7/19/2025 4:33pm :
  - Finished scoring system, Stock-Analyzer.py
    - Thanks to [Ayema](https://github.com/ayemaqu), [Kabbo](https://github.com/robinflew) for help with scoring code!
  - Created app.py
***

> [!WARNING]
>  This is not financial advice. Always do your own research before you purchase stocks.
