import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData

from exceptions import EquityTypeMismatchError
from exceptions import SectorError

import industries


class Stock:

    AV_API_KEY = 'AIDD24S6AW4MOOHG'

    def __init__(self, symbol):
        self.symbol = symbol

    def classify(self, sector, industry=None, subindustry=None):
        gics = industries.GICS(sector, industry, subindustry)
        return gics


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
