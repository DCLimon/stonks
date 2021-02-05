import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData

import industries
from equity import Stock
from industries import PeerComparison


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
                # ST Assets:
                'cash': 'Cash',
                'shortTermInvestments': 'ST Invest',
                'cashAndShortTermInvestments': 'Cash & ST Invest',
                'netReceivables': 'Net Receivables',
                'inventory': 'Inventory',
                'otherCurrentAssets': 'Oth Curr Asset',
                'totalCurrentAssets': 'Tot Curr Asset',
                # LT Assets:
                'accumulatedDepreciation': 'Accum Depreciation',
                'propertyPlantEquipment': 'PP&E',
                'goodwill': 'GW',
                'accumulatedAmortization': 'Accum Amort',
                'intangibleAssets': 'Intang Asset',
                'longTermInvestments': 'LT Invest',
                'otherNonCurrrentAssets': 'Oth Non-curr Asset',
                'totalNonCurrentAssets': 'Tot Non-curr Asset',
                'totalAssets': 'Tot Asset',
                # ST Lblts:
                'accountsPayable': 'Acct Payable',
                'shortTermDebt': 'ST Debt',
                'currentLongTermDebt': 'Curr LT Debt',
                'otherCurrentLiabilities': 'Oth Curr Lblts',
                'totalCurrentLiabilities': 'Tot Curr Lblts',
                # LT Lblts
                'longTermDebt': 'LT Debt',
                'totalLongTermDebt': 'Tot LT Debt',
                'deferredLongTermLiabilities': 'Defer LT Lblts',
                'otherNonCurrentLiabilities': 'Oth Non-curr Lblts',
                'totalNonCurrentLiabilities': 'Tot Non-curr Lblts',
                'otherLiabilities': 'Oth Lblts',
                'totalLiabilities': 'Tot Lblts',
                # SH Equity:
                'commonStock': 'Com Stock',
                'additionalPaidInCapital': 'Addl Paid in Cap',
                'commonStockTotalEquity': 'Com Stock Tot Eq',
                'retainedEarnings': 'Retain Earn',
                'treasuryStock': 'Treasury Stock',
                'otherShareholderEquity': 'Oth SH Eq',
                'totalShareholderEquity': 'Tot SH Eq',
                'liabilitiesAndShareholderEquity': 'Lblts & SH Eq',
                'commonStockSharesOutstanding': 'Com Shares Out',
                # Not yet organized:
                'earningAssets': 'Earning Asset',
                'otherAssets': 'Oth Asset',
                'netTangibleAssets': 'Net Tang Asset',
                'totalPermanentEquity': 'Tot Permanent Eq',
                'preferredStockTotalEquity': 'Pref Stock Tot Eq',
                'retainedEarningsTotalEquity': 'Retain Earn Tot Eq',
                'deferredLongTermAssetCharges': 'Def LT Asset Chrg',
                'capitalLeaseObligations': 'Cap Lease Obligation',
                'negativeGoodwill': 'Neg GW',
                'warrants': 'Warrants',
                'preferredStockRedeemable': 'Pref Stock Redeemable',
                'capitalSurplus': 'Cap Surplus',
            }, inplace=True
        )
        b_sheet.set_index('Fisc Period End',
                          drop=True,
                          append=False,
                          inplace=True)
        b_sheet.drop(columns=['Reported Currency'], inplace=True)

        return b_sheet


class Ratios(Overview, PeerComparison):

    def __init__(self, symbol, sector, industry=None, subindustry=None):
        Overview.__init__(self, symbol)
        PeerComparison.__init__(
            self, symbol, sector, industry=None, subindustry=None
        )

    def vs_peers(self, peer_level, *ratios):
        if peer_level == 'Sector':
            peer_list = self.sector_peers
        elif peer_level == 'Industry':
            peer_list = self.industry_peers
        elif peer_level == 'Sub-Industry':
            peer_list = self.subindustry_peers

        peer_df = pd.DataFrame(
            index=peer_list,
            columns=ratios
        )

        for peer in peer_list:
            ov = Overview(peer).overview
            ratio_dict = {}

            for ratio in ratios:
                ratio_dict[ratio] = ov[ratio]
            peer_series = pd.Series(ratio_dict, name=peer)
            peer_df.append(peer_series)

        ratio_series = pd.Series(
            [peer_df[ratio].mean for ratio in ratios],
            name=f"{self.symbol} Peers"
        )
        return ratio_series
