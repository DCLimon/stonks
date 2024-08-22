import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData

from exceptions import EquityTypeMismatchError
from exceptions import SectorError

import industries


def read_api_keys(file):
    try:
        with open(file, 'r') as f:
            api_keys = list(
                filter(None, [line.rstrip('\n') for line in f if line])
            )
            return {k: v for k, v in zip(api_keys[0::2], api_keys[1::2])}
    except FileNotFoundError:
        print(f'File "{file}" was not found')


class Stock:

    AV_API_KEY = read_api_keys('api_keys.txt')['alphavantage']
    
    def __init__(self, symbol):
        self.symbol = symbol

    # def classify(self, sector, industry=None, subindustry=None):
    #     gics = industries.GICS(sector, industry, subindustry)
    #     return gics


    # @property
    # def _metadata(self):
    #     # Make Series with all (raw) output from alpha_vantage json.
    #     raw = pd.Series(
    #         FundamentalData(
    #             key=Stock.AV_API_KEY, output_format='json'
    #         ).get_company_overview('MRK')[0]
    #     )
    #
    #     # Trim raw into only rows wanted as metadata.
    #     trimmed = raw[[
    #         'Symbol', 'Name', 'Description', 'Address', 'AssetType',
    #         'Currency', 'Country', 'Exchange', 'Sector', 'Industry',
    #         'FullTimeEmployees', 'FiscalYearEnd', 'LatestQuarter'
    #     ]]
    #     trimmed.index = [
    #         'Symbol', 'Name', 'Description', 'Address', 'Equity Type',
    #         'Currency', 'Country', 'Exchange', 'Sector', 'Industry',
    #         'Full-time Employees', 'FY End', 'Latest Quarter'
    #     ]
    #     trimmed.name = f'{self.symbol} Metadata'
    #
    #     return trimmed
