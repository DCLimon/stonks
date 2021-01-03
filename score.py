import datetime
from pprint import pprint

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries

# initialize av API
AV_API_KEY = 'AIDD24S6AW4MOOHG'
ts = TimeSeries(key=AV_API_KEY, output_format='pandas')

class Equity(object):

    tickerName = {
        # ticker:common_name
        'MMM': '3M',
        'HON': 'Honeywell',
        'GE': 'GE',
        'TEVA': 'Teva',
        'MDT': 'Medtronic',
        'F': 'Ford',
        'ABT': 'Abbott',
        'BA': 'Boeing',
        'EADSY': 'Airbus',
        'SLB': 'Schlumberger',
        'DAL': 'Delta',
        'UAL': 'United Airlines',
        'XOM': 'Exxon',
        'RTX': 'Raytheon',
        'LHX': 'L3Harris',
        'GD': 'General Dynamics',
        'WBA': 'Walgreens,',
        'VTRS': 'Viatris',
        'AAPL': 'Apple',
        'BDX': 'BD',
        'CVS': 'CVS',
        'HAL': 'Halliburton',
        'MSFT': 'Microsoft',
        'NVDA': 'Nvidia',
        'PFE': 'Pfizer',
        'RDS.B': 'Shell',
        'LUV': 'Southwest Airlines'
    }

    def __init__(self, ticker, equity_type='stock', exchange=None,
                 sector=None):
        self.ticker = ticker
        self.equity_type = equity_type
        self.exchange = exchange
        self.sector = sector

    @property
    def common_name(self):
        if self.ticker in Equity.tickerName:
            return Equity.tickerName[self.ticker]
        else:
            print('No common name defined for this ticker.\n')
            name = input('Enter common name: ')
            Equity.new_ticker(self.ticker, name)
            return Equity.tickerName[self.ticker]

    @staticmethod
    def new_ticker(ticker, name):
        Equity.tickerName[ticker] = name
        