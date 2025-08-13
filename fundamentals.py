import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData

import industries
from industries import PeerComparison


def read_api_keys(file):
    try:
        with open(file, 'r') as f:
            api_keys = list(
                filter(None, [line.rstrip('\n') for line in f if line])
            )
            return {k: v for k, v in zip(api_keys[0::2], api_keys[1::2])}
    except FileNotFoundError:
        print(f'File "{file}" was not found')


class Overview:
    AV_API_KEY = read_api_keys('apikeys.txt')['alpha_vantage']

    def __init__(self, symbol):
        self.symbol = symbol

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
        ov_data_series[ov_data_series == 'None'] = np.nan
        ov_data_series.astype('float64')

        return ov_data_series


class IncomeStatement:
    def __init__(self, obj):
        self._obj = obj


class BalanceSheet:
    AV_API_KEY = read_api_keys('apikeys.txt')['alpha_vantage']

    def __init__(self,
                 symbol: str,
                 freq: str = 'yearly',
                 periods: int = 5):
        self.symbol = symbol
        self.freq = freq
        self.periods = periods

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
        b_sheet = b_sheet.rename(
            columns={
                'fiscalDateEnding': 'fy_end',
                'reportedCurrency': 'report_currency',
                # ST Assets:
                'shortTermInvestments': 'st_invest',
                'cashAndShortTermInvestments': 'cash_st_invest',
                'netReceivables': 'ar_net',
                'otherCurrentAssets': 'oth_curr_asset',
                'totalCurrentAssets': 'tot_curr_asset',
                # LT Assets:
                'accumulatedDepreciation': 'accum_deprec',
                'propertyPlantEquipment': 'ppe',
                'goodwill': 'gw',
                'accumulatedAmortization': 'accum_amort',
                'intangibleAssets': 'intang_asset',
                'longTermInvestments': 'lt_invest',
                'otherNonCurrrentAssets': 'oth_noncurr_asset',
                'totalNonCurrentAssets': 'oth_noncurr_asset',
                'totalAssets': 'tot_asset',
                # ST Lblts:
                'accountsPayable': 'ap',
                'shortTermDebt': 'st_debt',
                'currentLongTermDebt': 'curr_lt_debt',
                'otherCurrentLiabilities': 'oth_curr_lblt',
                'totalCurrentLiabilities': 'tot_curr_lblt',
                # LT Lblts
                'longTermDebt': 'lt_debt',
                'totalLongTermDebt': 'tot_lt_debt',
                'deferredLongTermLiabilities': 'def_lt_lblt',
                'otherNonCurrentLiabilities': 'oth_noncurr_lblt',
                'totalNonCurrentLiabilities': 'tot_noncurr_lblt',
                'otherLiabilities': 'oth_blt',
                'totalLiabilities': 'tot_lblt',
                # SH Equity:
                'commonStock': 'comm_stock',
                'additionalPaidInCapital': 'apic',
                'commonStockTotalEquity': 'comm_stock_tot_eq',
                'retainedEarnings': 'ret_earn',
                'treasuryStock': 'treasury_stock',
                'otherShareholderEquity': 'oth_SH_eq',
                'totalShareholderEquity': 'tot_SH_eq',
                'liabilitiesAndShareholderEquity': 'lblt_SH_eq',
                'commonStockSharesOutstanding': 'comm_shares_out',
                # Not yet organized:
                'earningAssets': 'earning_asset',
                'otherAssets': 'oth_asset',
                'netTangibleAssets': 'net_tang_asset',
                'totalPermanentEquity': 'tot_perm_eq',
                'preferredStockTotalEquity': 'pref_stock_tot_eq',
                'retainedEarningsTotalEquity': 'ret_earn_tot_eq',
                'deferredLongTermAssetCharges': 'def_LT_asset_charge',
                'capitalLeaseObligations': 'cap_lease_obligation',
                'negativeGoodwill': 'neg_gw',
                'preferredStockRedeemable': 'pref_stock_redeemable',
                'capitalSurplus': 'cap_surplus',
            }
        )
        b_sheet = b_sheet.set_index('Fisc Period End',
                          drop=True,
                          append=False)
        b_sheet = b_sheet.drop(columns=['Reported Currency'])

        return b_sheet


class Ratios(PeerComparison):

    def __init__(self, symbol, sector, industry=None, subindustry=None):
        super().__init__(symbol, sector, industry, subindustry)

    def vs_peers(self, peer_level, *ratios):
        if peer_level == 'Sector':
            peer_list = self.sector_peers
        elif peer_level == 'Industry':
            peer_list = self.industry_peers
        elif peer_level == 'Sub-Industry':
            peer_list = self.subindustry_peers

        peer_df = pd.DataFrame(
            columns=ratios
        )

        for peer in peer_list:
            ov = Overview(peer).overview
            ratio_dict = {}

            for ratio in ratios:
                ratio_dict[ratio] = ov[ratio]

            peer_series = pd.Series(ratio_dict, name=peer)
            peer_df = peer_df.append(peer_series)
            print(peer_series)

        # print(peer_df)
        # ratio_series = pd.Series(
        #     [peer_df[ratio].mean() for ratio in ratios],
        #     name=f"{self.symbol} Peers"
        # )
        return peer_df


xom_ratios = Ratios('XOM', 'Energy', 'Oil, Gas & Consumable Fuels',
                    'Integrated Oil & Gas')
op = xom_ratios.vs_peers('Sub-Industry', 'P/E', 'P/B', 'TTM ROE')
