from flask import Flask, render_template, request
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from Stock_Analyzer import StockAnalyzer


