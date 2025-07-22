from flask import Flask, render_template, request
from Stock_Analyzer import StockAnalyzer

stock = StockAnalyzer()
stock.run_all()