import json
import requests
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import polars as pl
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData

# from fundamentals import IncomeStatement


# from exceptions import EquityTypeMismatchError
# from exceptions import SectorError
#
# import industries


def get_api_key(api: str, key_file: Path = None) -> str:
    if key_file is None:
        key_file = Path.cwd() / 'apikeys.json'

    try:
        with open(key_file, 'r') as f:
            keys = json.load(f)
            key = keys[api]
            return key
    except FileNotFoundError:
        print(f'File "{key_file}" was not found')


class AVRequest:
    API = 'alpha_vantage'

    def __init__(self, fn: str, symbol: str, api_key: Optional[str] = None):
        self.fn = fn.upper()
        self.symbol = symbol.upper()
        self.api_key = api_key

    @property
    def url(self):
       return f'https://www.alphavantage.co/query?function={self.fn}&symbol={self.symbol}&apikey={self.api_key}'

    def output(self, output_format: str = 'json'):
        result = requests.get(self.url).json()

        if output_format == 'json':
            return result
        elif output_format == 'pandas':
            return pd.Series(result)


class Stock:
    def __init__(self, symbol: str,  api_key: Optional[str] = None):
        self.symbol = symbol.upper()
        self.api_key = api_key

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        if value is None:
            self._api_key = get_api_key('alpha_vantage')
        else:
            self._api_key = value

    # def classify(self, sector, industry=None, subindustry=None):
    #     gics = industries.GICS(sector, industry, subindustry)
    #     return gics

    def get_overview(self) -> pl.DataFrame:
        # Make Series with all (raw) output from alpha_vantage json.
        ov = FundamentalData(
            key=self.api_key, output_format='json'
        ).get_company_overview(self.symbol)[0].iloc[0]

        # Trim raw into only rows wanted as metadata.
        # trimmed = ov[[
        #     'Symbol', 'Name', 'Description', 'Address', 'AssetType',
        #     'Currency', 'Country', 'Exchange', 'Sector', 'Industry',
        #     'FullTimeEmployees', 'FiscalYearEnd', 'LatestQuarter'
        # ]]
        # trimmed.index = [
        #     'Symbol', 'Name', 'Description', 'Address', 'Equity Type',
        #     'Currency', 'Country', 'Exchange', 'Sector', 'Industry',
        #     'Full-time Employees', 'FY End', 'Latest Quarter'
        # ]
        # trimmed.name = f'{self.symbol} Metadata'

        return pl.DataFrame(ov)

    def get_income_statement(self):
        inc_stmt = (
            FundamentalData(key=self.api_key, output_format='json')
            .get_income_statement_annual(self.symbol)[0]
        )

        return pl.from_pandas(inc_stmt)

    def get_balance_sheet(self):
        bs = (
            FundamentalData(key=self.api_key, output_format='json')
            .get_balance_sheet_annual(self.symbol)[0]
        )

        return pl.from_pandas(bs)

    def get_cash_flow_statement(self):
        scf = (
            FundamentalData(key=self.api_key, output_format='json')
            .get_cash_flow_annual(self.symbol)
        )

        return scf


class DemoStock(Stock):
    def __init__(self):
        self._json_folder_path = Path.cwd() / 'request_db'
        super().__init__(symbol='ISRG',  # IBM used for online API
                         api_key='Demo')
        self.overview = None
        self.income_statement = None
        self.balance_sheet = None
        self.cash_flow_statement = None

    @property
    def overview(self):
        return self._overview

    @overview.setter
    def overview(self, value):
        if value is None:
            self._overview = self.get_overview()
        else:
            self._overview = value

    def get_overview(self):
        # Use AV's demo result
        # ov = AVRequest(fn='OVERVIEW', symbol='IBM', api_key='Demo').output()

        # Load from saved json
        ov = pl.read_json(self._json_folder_path / 'ISRG_ov_2025-03-22.json')
        return pl.DataFrame(ov)

    @property
    def income_statement(self):
        return self._income_statement

    @income_statement.setter
    def income_statement(self, value):
        if value is None:
            self._income_statement = self.get_income_statement()
        else:
            self._income_statement = value

    def get_income_statement(self):
        # inc = (
        #     AVRequest(fn='INCOME_STATEMENT', symbol='IBM', api_key='Demo')
        #     .output()
        # )
        inc = pl.read_json(self._json_folder_path / 'ISRG_is_2025-04-11.json')

        non_int_cols = ['fiscalDateEnding', 'reportedCurrency']

        inc = (
            inc
            .with_columns([
                pl.col(col).replace("None", None)
                for col in inc.columns
            ])
            .with_columns([
                pl.col('fiscalDateEnding')
                .str.strptime(pl.Date, '%Y-%m-%d')
            ])
            .with_columns([
                pl.col(col).cast(pl.Int64).fill_null(0) for col in inc.columns
                if col not in non_int_cols
            ])

        )

        return inc

    @property
    def balance_sheet(self):
        return self._balance_sheet

    @balance_sheet.setter
    def balance_sheet(self, value):
        if value is None:
            self._balance_sheet = self.get_balance_sheet()
        else:
            self._balance_sheet = value

    def get_balance_sheet(self):
        non_int_cols = ['fiscalDateEnding', 'reportedCurrency']

        bs = pl.read_json(self._json_folder_path / 'ISRG_bs_2025-04-14.json')

        bs = (
            bs
            .with_columns([
                pl.col(col).replace("None", None)
                for col in bs.columns
            ])
            .with_columns([
                pl.col('fiscalDateEnding')
                .str.strptime(pl.Date, '%Y-%m-%d')
            ])
            .with_columns([
                pl.col(col).cast(pl.Int64).fill_null(0) for col in bs.columns
                if col not in non_int_cols
            ])

        )

        return bs

    @property
    def cash_flow_statement(self):
        return self._cash_flow_statement

    @cash_flow_statement.setter
    def cash_flow_statement(self, value):
        if value is None:
            self._cash_flow_statement = self.get_cash_flow_statement()
        else:
            self._cash_flow_statement = value

    def get_cash_flow_statement(self):
        scf = pl.read_json(self._json_folder_path / 'ISRG_scf_2025-05-18.json')

        non_int_cols = ['fiscalDateEnding', 'reportedCurrency']

        scf = (
            scf
            .with_columns([
                pl.col(col).replace("None", None)
                for col in scf.columns
            ])
            .with_columns([
                pl.col('fiscalDateEnding')
                .str.strptime(pl.Date, '%Y-%m-%d')
            ])
            .with_columns([
                pl.col(col).cast(pl.Int64).fill_null(0) for col in scf.columns
                if col not in non_int_cols
            ])

        )

        return scf


def dump_to_json(df: pl.DataFrame, path: Path, indent: int = 2) -> None:
    with open(path, 'w') as f:
        json.dump(json.loads(df.write_json()), f, indent=indent)
    print(f'File written to: {path.parent}')


def main():
    global isrg_demo, is_xpose, bs_xpose, cfs_xpose
    isrg_demo = DemoStock()
    is_xpose = isrg_demo.income_statement.transpose(include_header=True)
    bs_xpose = isrg_demo.balance_sheet.transpose(include_header=True)
    cfs_xpose = isrg_demo.cash_flow_statement.transpose(include_header=True)
    # global ibm
    # ibm = DemoStock()


if __name__ == '__main__':
    main()
