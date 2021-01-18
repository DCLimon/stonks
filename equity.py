import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData

from exceptions import EquityTypeMismatchError
from exceptions import SectorError

import industries


class Equity(object):

    AV_API_KEY = 'AIDD24S6AW4MOOHG'

    def __init__(self, symbol, equity_type, exchange=None,
                 sector=None):
        self.symbol = symbol
        self.equity_type = equity_type
        self.exchange = exchange
        self.sector = sector

    # @property
    # def common_name(self):
    #     if self.symbol in Equity.symbol_name:
    #         return Equity.symbol_name[self.symbol]
    #     else:
    #         print('No common name defined for this symbol.\n')
    #         name = input('Enter common name: ')
    #         Equity.new_symbol(self.symbol, name)
    #         return Equity.symbol_name[self.symbol]
    #
    # @staticmethod
    # def new_symbol(symbol, name):
    #     Equity.symbol_name[symbol] = name


class Stock:

    def __init__(self, symbol):
        self.symbol = symbol
        # super().__init__(symbol, equity_type)
        # self.equity_type = 'Stock'
        # self.sector = sector
        # self.industry = industry
        # self.subindustry = subindustry

    def classify(self, sector, industry=None, subindustry=None):
        gics = industries.GICS(sector, industry, subindustry)
        return gics

    # @property
    # def equity_type(self):
    #     if 'Stock' in self._metadata()['Equity Type']:
    #         return 'Stock'
    #     else:
    #         raise EquityTypeMismatchError(class_instance='Stock')

    # @property
    # def exchange(self):
    #     return self._metadata['Exchange']
    #
    # @property
    # def sector(self):
    #     return self._metadata['Sector']
    #
    # @sector.setter
    # def sector(self, value):
    #     self._sp500 = industries.GICS(self.symbol, value)
    #
    # @property
    # def industry(self):
    #     return self._metadata['Industry']
    #
    # @property
    # def name(self):
    #     return self._metadata['Name']

    @property
    def _metadata(self):
        # Make Series with all (raw) output from alpha_vantage json.
        raw = pd.Series(
            FundamentalData(
                key=Stock.AV_API_KEY, output_format='json'
            ).get_company_overview('MRK')[0]
        )

        # Trim raw into only rows wanted as metadata.
        trimmed = raw[[
            'Symbol', 'Name', 'Description', 'Address', 'AssetType',
            'Currency', 'Country', 'Exchange', 'Sector', 'Industry',
            'FullTimeEmployees', 'FiscalYearEnd', 'LatestQuarter'
        ]]
        trimmed.index = [
            'Symbol', 'Name', 'Description', 'Address', 'Equity Type',
            'Currency', 'Country', 'Exchange', 'Sector', 'Industry',
            'Full-time Employees', 'FY End', 'Latest Quarter'
        ]
        trimmed.name = f'{self.symbol} Metadata'

        return trimmed
