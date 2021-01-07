import datetime
from pprint import pprint

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries

# initialize av API
AV_API_KEY = 'AIDD24S6AW4MOOHG'
ts = TimeSeries(key=AV_API_KEY, output_format='pandas')

symbolName = {
        # symbol:common_name
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


class Equity(object):

    def __init__(self, symbol, equity_type='stock', exchange=None,
                 sector=None):
        self.symbol = symbol
        self.equity_type = equity_type
        self.exchange = exchange
        self.sector = sector

    @property
    def common_name(self):
        if self.symbol in Equity.symbolName:
            return Equity.symbolName[self.symbol]
        else:
            print('No common name defined for this symbol.\n')
            name = input('Enter common name: ')
            Equity.new_symbol(self.symbol, name)
            return Equity.symbolName[self.symbol]

    @staticmethod
    def new_symbol(symbol, name):
        Equity.symbolName[symbol] = name
