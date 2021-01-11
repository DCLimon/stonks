import pandas as pd
import numpy as np

from equity import Stock

stock_sector_series = pd.read_csv(
    'sp500_constituents.csv',
    header=None,
    names=['Sector', 'Symbol'],
    index_col='Symbol',
    squeeze=True  # Returns Series <=> data only has 1 column (o/w
                  # will return a 1-column df object.
)

# raw_struc has no repeated values, so produces many Nan cells.
raw_struc = pd.read_csv(
    'gics_struc.csv',
    header=0,
    names=['Sector', 'Industry Group', 'Industry', 'Sub-Industry'],
    index_col=None,
)

for row in np.arange(1, raw_struc.index.size):
    for column in raw_struc.columns:
        if raw_struc.isna().iloc[row][column]:
            raw_struc.iloc[row][column] = raw_struc.iloc[row-1][column]

# Make a MultiIndex object; take raw_struc column Series, remove NaN
# cells, then take values as lists to use in MultiIndex.from_product().
gics_index = pd.MultiIndex.from_product(
    [
        raw_struc['Sector'].dropna().values,
        raw_struc['Industry Group'].dropna().values,
        raw_struc['Industry'].dropna().values,
        raw_struc['Sub-Industry'].dropna().values
    ]
)


class GICS:

    _sp500_stock_list = stock_sector_series.index.values

    # planned df for GICS Sector/Industry/Sub-industry/etc. structure
    # _structure = pd.DataFrame()
