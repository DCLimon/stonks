import datetime
from pprint import pprint

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData

from exceptions import EquityTypeMismatchError
from exceptions import SectorError


class Equity(object):

    AV_API_KEY = 'AIDD24S6AW4MOOHG'

    symbol_name = {
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

    def __init__(self, symbol, equity_type, exchange=None,
                 sector=None):
        self.symbol = symbol
        self.equity_type = equity_type
        self.exchange = exchange
        self.sector = sector

    @property
    def common_name(self):
        if self.symbol in Equity.symbol_name:
            return Equity.symbol_name[self.symbol]
        else:
            print('No common name defined for this symbol.\n')
            name = input('Enter common name: ')
            Equity.new_symbol(self.symbol, name)
            return Equity.symbol_name[self.symbol]

    @staticmethod
    def new_symbol(symbol, name):
        Equity.symbol_name[symbol] = name


class Stock(Equity):

    def __init__(self, symbol):
        super().__init__(symbol)

    @property
    def equity_type(self):
        if 'Stock' in self._metadata()['Equity Type']:
            return 'Stock'
        else:
            raise EquityTypeMismatchError(class_instance='Stock')

    @property
    def exchange(self):
        return self._metadata()['Exchange']

    @property
    def sector(self):
        return self._metadata()['Sector']

    @property
    def industry(self):
        return self._metadata()['Industry']

    @property
    def name(self):
        return self._metadata()['Name']

    def _metadata(self):
        # Make Series with all (raw) output from alpha_vantage json.
        raw = pd.Series(
            FundamentalData(
                key=Stock.AV_API_KEY, output_format='json'
            ).get_company_overview('MRK')[0]
        )

        # Trim raw into only rows wanted as metadata.
        trimmed = raw[[
            'Symbol',
            'Name',
            'Description',
            'Address',
            'AssetType',
            'Currency',
            'Country',
            'Exchange',
            'Sector',
            'Industry',
            'FullTimeEmployees',
            'FiscalYearEnd',
            'LatestQuarter'
        ]]
        trimmed.index = [
            'Symbol',
            'Name',
            'Description',
            'Address',
            'Equity Type',
            'Currency',
            'Country',
            'Exchange',
            'Sector',
            'Industry',
            'Full-time Employees',
            'FY End',
            'Latest Quarter'
        ]
        trimmed.name = f'{self.symbol} Metadata'

        return trimmed



class MarketSector:

    # simple_name: detailed_name
    sectors = [
        'Consumer Discretionary',
        'Real Estate',
        'Utilities',
        'Information Technology',
        'Consumer Staples',
        'Health Care',
        'Communication Services',
        'Energy',
        'Financials',
        'Industrials',
        'Materials'
    ]

    def __init__(self, sector):
        if sector in self.sectors:
            self._sector = sector
        else:
            raise SectorError(f'sector must be in MarketSector.sectors')


_sectors = {
    'consumer discretionary': 'Consumer Discretionary',
    'real estate': 'Real Estate',
    'utilities': 'Utilities',
    'it': 'Information Technology',
    'staples': 'Consumer Staples',
    'health': 'Health Care',
    'comms': 'Communication Services',
    'energy': 'Energy',
    'finance': 'Financials',
    'industrial': 'Industrials',
    'materials': 'Materials'
}
