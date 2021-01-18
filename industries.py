import pandas as pd
import numpy as np

from equity import Stock

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

    def __init__(self, level, group):

        if not GICS._industry_struc.columns.str.contains(level).any:
            raise ValueError("Invalid value for level: must be "
                             "'Sector', 'Industry', or 'Sub-Industry'.")
        elif not GICS._industry_struc[level].str.contains(group).any():
            # Check that 'group' exists within 'level', e.g.
            # 'Shoemaking' is not a valid GICS Sector.
            raise ValueError("Specified 'group' value is not an valid "
                             "type of 'level'.")
        elif level == 'Sector':
            self.sector = group
        elif level == 'Industry':
            self.industry = group
            self.sector = GICS._industry_struc.loc[
                GICS._industry_struc[
                    'Industry'
                ]
                == self.industry, 'Sector'
            ].iloc[0]
        elif level == 'Sub-Industry':
            self.subindustry = group
            self.industry = GICS._industry_struc.loc[
                GICS._industry_struc[
                    'Sub-Industry'
                ]
                == self.subindustry, 'Industry'
            ].iloc[0]
            self.sector = GICS._industry_struc.loc[
                GICS._industry_struc[
                    'Industry'
                ]
                == self.subindustry, 'Sector'
            ].iloc[0]
