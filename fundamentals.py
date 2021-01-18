import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData

import industries
from equity import Stock


class Overview(Stock):
    def __init__(self, symbol, equity_type):
        super().__init__(symbol, equity_type)
        self.equity_type = 'Stock'


    @property
    def overview(self):
        ov_data_series = pd.Series(
            FundamentalData(
                key=Overview.AV_API_KEY, output_format='json'
            ).get_company_overview(self.symbol)[0]
        )

        ov_data_series = ov_data_series.drop(labels=[
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
        ])
        ov_data_series.index = [
            'Market Cap', 'EBITDA', 'P/E', 'PEG', 'BV', 'DPS',
            'Div Yield', 'EPS', 'TTM RPS', 'Net Prof Margin',
            'TTM Op Margin', 'TTM ROA', 'TTM ROE', 'TTM Rev',
            'TTM Gross Prof', 'TTM Diluted EPS',
            'YOY Q Earnings Growth', 'YOY Q Rev Growth',
            'Analyst Target Price', 'Trailing P/E', 'Forward P/E',
            'TTM P/S', 'P/B', 'EV/Rev', 'EV/EBITDA', 'Beta',
            '52 Wk High', '52 Wk Low', 'SMA50', 'SMA200',
            'Shares Outstanding', 'Shares Float', 'Shares Short',
            'Shares Short Prior Month', 'Short Ratio',
            'Short % Outstanding', 'Short % Float', '% Insiders',
            '% Institutions', 'Fwd Ann Div Rate',
            'Fwd Annual Div Yield', 'Payout Ratio', 'Div Date',
            'Ex-Div Date', 'Last Split Factor', 'Last Split Date'
        ]
        ov_data_series.name = self.symbol

        return ov_data_series


class BalanceSheet(Overview):
    def __init__(self, symbol, equity_type):
        super().__init__(symbol, equity_type)
        self.equity_type = 'Stock'

    @property
    def balance_sheet(self):
        b_sheet = pd.DataFrame(
            FundamentalData(
                key=Overview.AV_API_KEY, output_format='json'
            ).get_balance_sheet_quarterly(self.symbol)[0]
        )

        b_sheet.rename(
            columns={
                'fiscalDateEnding': 'Fisc Period End',
                'reportedCurrency': 'Reported Currency',
                'totalAssets': 'Tot Asset',
                'intangibleAssets': 'Intang Asset',
                'earningAssets': 'Earning Asset',
                'otherCurrentAssets': 'Oth Curr Asset',
                'totalLiabilities': 'Tot Liab',
                'totalShareholderEquity': 'Tot SH EQ',
                'deferredLongTermLiabilities': 'Defer LT Liab',
                'otherCurrentLiabilities': 'Oth Curr Liab',
                'otherNonCurrentLiabilities': 'Oth Non-curr Liab',
                'totalNonCurrentLiabilities': 'Tot Non-curr Liab',
                'negativeGoodwill': 'Neg Goodwill',
                'warrants': 'Warrants',
                'preferredStockRedeemable': 'Pref Stock Redeemable',
                'capitalSurplus': 'Cap Surplus',
                'liabilitiesAndShareholderEquity': 'Liab & SH EQ',
                'cashAndShortTermInvestments': 'Cash & ST Invest',
                'accumulatedDepreciation': 'Accum Depreciation',
                'commonStockSharesOutstanding': 'Common Shares Out'
            }, inplace=True
        )
        b_sheet.set_index('Fisc Period End',
                          drop=True,
                          append=False,
                          inplace=True)
        b_sheet.drop(columns=['Reported Currency'])


