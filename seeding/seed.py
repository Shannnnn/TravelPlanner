from odo import odo, dshape
import pandas as pd
from config import seedcountrystring, seedcitystring


ds = dshape("var * {countryID: int64, countryName: string, countryCode: string}")
odo("sample.csv", pd.DataFrame, dshape=ds)
odo("sample.csv", seedcountrystring)

ds = dshape("var * {countryID: int64, countryName: string, countryCode: string}")
odo("sample2.csv", pd.DataFrame, dshape=ds)
odo("sample2.csv", seedcitystring)