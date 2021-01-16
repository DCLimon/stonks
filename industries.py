import pandas as pd
import numpy as np

from equity import Stock

# from .csv, read in a Series where index is the symbols of all
# constituents of S&P 500 index.
_sp500_sectors = pd.read_csv(
    'sp500_constituents.csv',
    header=0,
    names=['Symbol', 'GICS Sector', 'GICS Sub-Industry'],
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

    Poor data source formatting for nested index data where higher-level
    columns do not repeat their values in every applicable row creates a
    df with many NaN cells. This is unusable as in column nor is it
    easily converted to a MultiIndex. MultiIndex.from_product()
    creates factorial/crossed index: ALL levels of subordinate
    indices repeat at EVERY level of a higher-order index, e.g. EVERY
    level of mammal_species has BOTH levels of sub-index 'sex' (M & F).

    See gics_struc.csv for example of poorly formatted nested data. In
    nested data/indices, levels of a sub-index are are unique to the
    level of the higher-order index under which it falls. In the example
    of gics_struc, the 'Pharmaceuticals' Industry only occurs within the
    'Health Care' Sector, while the IT Sector has its own unique set of
    Industries.
    """
    for row in np.arange(1, df.index.size):
        for column in df.columns:
            if df.isna().iloc[row][column]:
                df.iloc[row][column] = df.iloc[row-1][column]
    return df





class GICS:

    # Fill all _gics_struc rows with appropriate column data.
    _industry_struc = _fill_nested_df(_gics_struc)

    _sp500_stock_list = _sp500_sectors.index.values

    # planned df for GICS Sector/Industry/Sub-industry/etc. structure
    # _structure = pd.DataFrame()
