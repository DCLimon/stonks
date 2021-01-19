import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData

import industries
from equity import Stock


class Overview(Stock):
    def __init__(self, symbol):
        super().__init__(symbol)

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


class BalanceSheet(Stock):
    def __init__(self, symbol, freq='quarterly', periods=5):
        super().__init__(symbol)
        self.freq = freq
        self.periods = periods

    @property
    def balance_sheet(self):
        if self.freq == 'quarterly':
            b_sheet = pd.DataFrame(
                FundamentalData(
                    key=BalanceSheet.AV_API_KEY, output_format='json'
                ).get_balance_sheet_quarterly(self.symbol)[0]
            )
        elif self.freq == ('annual' or 'yearly'):
            b_sheet = pd.DataFrame(
                FundamentalData(
                    key=BalanceSheet.AV_API_KEY, output_format='json'
                ).get_balance_sheet_annual(self.symbol)[0]
            )
        else:
            raise ValueError("'freq' attribute must be 'quarterly' "
                             "or 'annual'")

        b_sheet = b_sheet.iloc[:self.periods]
        b_sheet.rename(
            columns={
                'fiscalDateEnding': 'Fisc Period End',
                'reportedCurrency': 'Reported Currency',
                'totalAssets': 'Tot Asset',
                'intangibleAssets': 'Intang Asset',
                'earningAssets': 'Earning Asset',
                'otherCurrentAssets': 'Oth Curr Asset',
                'totalLiabilities': 'Tot Lblts',
                'totalShareholderEquity': 'Tot SH Eq',
                'deferredLongTermLiabilities': 'Defer LT Lblts',
                'otherCurrentLiabilities': 'Oth Curr Lblts',
                'commonStock': 'Com Stock',
                'retainedEarnings': 'Retain Earn',
                'otherLiabilities': 'Oth Lblts',
                'goodwill': 'GW',
                'otherAssets': 'Oth Asset',
                'cash': 'Cash',
                'totalCurrentLiabilities': 'Tot Curr Lblts',
                'shortTermDebt': 'ST Debt',
                'currentLongTermDebt': 'Curr LT Debt',
                'otherShareholderEquity': 'Oth SH Eq',
                'propertyPlantEquipment': 'Prop/Plant/Equip',
                'totalCurrentAssets': 'Tot Curr Asset',
                'longTermInvestments': 'LT Invest',
                'netTangibleAssets': 'Net Tang Asset',
                'shortTermInvestments': 'ST Invest',
                'netReceivables': 'Net Receivables',
                'longTermDebt': 'LT Debt',
                'inventory': 'Inventory',
                'accountsPayable': 'Acct Payable',
                'totalPermanentEquity': 'Tot Permanent Eq',
                'additionalPaidInCapital': 'Addl Paid in Cap',
                'commonStockTotalEquity': 'Com Stock Tot Eq',
                'preferredStockTotalEquity': 'Pref Stock Tot Eq',
                'retainedEarningsTotalEquity': 'Retain Earn Tot Eq',
                'treasuryStock': 'Treasury Stock',
                'accumulatedAmortization': 'Accum Amort',
                'otherNonCurrrentAssets': 'Oth Non-curr Asset',
                'deferredLongTermAssetCharges': 'Def LT Asset Chrg',
                'totalNonCurrentAssets': 'Tot Non-curr Asset',
                'capitalLeaseObligations': 'Cap Lease Obligation',
                'totalLongTermDebt': 'Tot LT Debt',
                'otherNonCurrentLiabilities': 'Oth Non-curr Lblts',
                'totalNonCurrentLiabilities': 'Tot Non-curr Lblts',
                'negativeGoodwill': 'Neg GW',
                'warrants': 'Warrants',
                'preferredStockRedeemable': 'Pref Stock Redeemable',
                'capitalSurplus': 'Cap Surplus',
                'liabilitiesAndShareholderEquity': 'Lblts & SH Eq',
                'cashAndShortTermInvestments': 'Cash & ST Invest',
                'accumulatedDepreciation': 'Accum Depreciation',
                'commonStockSharesOutstanding': 'Com Shares Outstanding'
            }, inplace=True
        )
        b_sheet.set_index('Fisc Period End',
                          drop=True,
                          append=False,
                          inplace=True)
        b_sheet.drop(columns=['Reported Currency'], inplace=True)

        b_sheet_index = pd.MultiIndex.from_frame(pd.DataFrame(
            [
                ['Assets', 'Cash & ST Invest' ,'Cash & Equiv'],
                ['Assets', 'Cash & ST Invest', 'ST Invest'],
                ['Assets', 'Cash & ST Invest', 'Cash & ST Invest'],

            ]
        ))

        return b_sheet

'totalAssets': 'Tot Asset',
'intangibleAssets': 'Intang Asset',
'earningAssets': 'Earning Asset',
'otherCurrentAssets': 'Oth Curr Asset',
'totalLiabilities': 'Tot Lblts',
'totalShareholderEquity': 'Tot SH Eq',
'deferredLongTermLiabilities': 'Defer LT Lblts',
'otherCurrentLiabilities': 'Oth Curr Lblts',
'commonStock': 'Com Stock',
'retainedEarnings': 'Retain Earn',
'otherLiabilities': 'Oth Lblts',
'goodwill': 'GW',
'otherAssets': 'Oth Asset',
'totalCurrentLiabilities': 'Tot Curr Lblts',
'shortTermDebt': 'ST Debt',
'currentLongTermDebt': 'Curr LT Debt',
'otherShareholderEquity': 'Oth SH Eq',
'propertyPlantEquipment': 'Prop/Plant/Equip',
'totalCurrentAssets': 'Tot Curr Asset',
'longTermInvestments': 'LT Invest',
'netTangibleAssets': 'Net Tang Asset',
'netReceivables': 'Net Receivables',
'longTermDebt': 'LT Debt',
'inventory': 'Inventory',
'accountsPayable': 'Acct Payable',
'totalPermanentEquity': 'Tot Permanent Eq',
'additionalPaidInCapital': 'Addl Paid in Cap',
'commonStockTotalEquity': 'Com Stock Tot Eq',
'preferredStockTotalEquity': 'Pref Stock Tot Eq',
'retainedEarningsTotalEquity': 'Retain Earn Tot Eq',
'treasuryStock': 'Treasury Stock',
'accumulatedAmortization': 'Accum Amort',
'otherNonCurrrentAssets': 'Oth Non-curr Asset',
'deferredLongTermAssetCharges': 'Def LT Asset Chrg',
'totalNonCurrentAssets': 'Tot Non-curr Asset',
'capitalLeaseObligations': 'Cap Lease Obligation',
'totalLongTermDebt': 'Tot LT Debt',
'otherNonCurrentLiabilities': 'Oth Non-curr Lblts',
'totalNonCurrentLiabilities': 'Tot Non-curr Lblts',
'negativeGoodwill': 'Neg GW',
'warrants': 'Warrants',
'preferredStockRedeemable': 'Pref Stock Redeemable',
'capitalSurplus': 'Cap Surplus',
'liabilitiesAndShareholderEquity': 'Lblts & SH Eq',
'accumulatedDepreciation': 'Accum Depreciation',
'commonStockSharesOutstanding': 'Com Shares Outstanding'
