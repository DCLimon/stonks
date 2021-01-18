import pandas as pd
import numpy as np

_sp500_sectors = pd.read_csv(
    # from .csv, read in a Series where index is the symbols of all
    # constituents of S&P 500 index.
    'sp500_constituents.csv',
    header=0,
    names=['Symbol', 'Sector', 'Industry Group', 'Industry',
           'Sub-Industry'],
    index_col='Symbol',
    squeeze=True  # Return Series <=> 1 data column (o/w returns df).
)


# .csv columns are nested data (Each Sector has unique set of
# Industries, which has unique set of Sub-Industries), but higher-level
# columns do not repeat their data in every applicable row. This leaves
# many rows with NaN data, & unusable as column or a MultiIndex.
_gics_struc = pd.read_csv(
    # Nested data structure formatted poorly in source file, giving many
    # blank/NaN cells; more info in _fill_nested_df() docstring.
    'gics_struc.csv',
    header=0,
    names=['Sector', 'Industry Group', 'Industry', 'Sub-Industry'],
    index_col=None,
)


def _fill_nested_df(df):
    """Fill all rows within columns represented nested data.

    Poor data source formatting for nested index data where  higher
    -level columns do not repeat their values in every applicable
    row creates a df with many NaN cells. This is unusable as in
    column nor is it easily converted to a MultiIndex.
    MultiIndex.from_product() creates factorial/crossed index: ALL
    levels of subordinate indices repeat at EVERY level of a higher-
    order index, e.g. EVERY level of mammal_species has BOTH levels
    of sub-index 'sex' (M & F).

    See gics_struc.csv for example of poorly formatted nested  data.
    In nested data/indices, levels of a sub-index are are unique to
    the level of the higher-order index under which it falls. In the
    example of gics_struc, the 'Pharmaceuticals' Industry only
    occurs within the 'Health Care' Sector,  while the
    IT Sector has its own unique set of Industries.
    """
    for row in np.arange(1, df.index.size):
        for column in df.columns:
            if df.isna().iloc[row][column]:
                df.iloc[row][column] = df.iloc[row - 1][column]
    return df


class GICS:

    # Fill all _gics_struc rows with appropriate column data.
    _industry_struc = _fill_nested_df(_gics_struc)

    _sp500_stock_list = _sp500_sectors.index.values

    def __init__(self, sector, industry=None, subindustry=None):
        self.sector = sector
        self.industry = industry
        self.subindustry = subindustry

    @property
    def sector(self):
        return self._sector

    @sector.setter
    def sector(self, value):
        if not (GICS._industry_struc['Sector'] == value).any():
            raise ValueError("'sector' must be valid GICS Sector.")
        else:
            self._sector = value

    @property
    def industry(self):
        return self._industry

    @industry.setter
    def industry(self, value):
        if not value:
            self._industry = None
        elif not (GICS._industry_struc['Industry'] == value).any():
            raise ValueError("'industry' must be valid GICS Industry.")
        else:
            self._industry = value

    @property
    def subindustry(self):
        return self._subindustry

    @subindustry.setter
    def subindustry(self, value):
        if not value:
            self._subindustry = None
        elif not (GICS._industry_struc['Sub-Industry'] == value).any():
            raise ValueError("'subindustry' must be valid GICS"
                             "Sub-Industry.")
        else:
            self._subindustry = value

            if not self.industry:
                # If subindustry but not industry argument is specified,
                # find & set proper industry attribute value.
                self.industry = GICS._industry_struc.loc[
                    GICS._industry_struc[
                        'Sub-Industry'
                    ] == self.subindustry, 'Industry'
                ].iloc[0]


class IndustryComparison(GICS):
    def __init__(self, sector, industry=None, subindustry=None):
        super().__init__(sector, industry, subindustry)

    @property
    def sector_partners(self):
        return _sp500_sectors.loc[
            _sp500_sectors['Sector'] == self.sector
        ].index

    @property
    def industry_partners(self):
        if not self.industry:
            return None
        else:
            return _sp500_sectors.loc[
                _sp500_sectors['Industry'] == self.industry
            ].index

    @property
    def subindustry_partners(self):
        if not self.subindustry:
            return None
        else:
            return _sp500_sectors.loc[
                _sp500_sectors['Sub-Industry'] == self.subindustry
            ].index
