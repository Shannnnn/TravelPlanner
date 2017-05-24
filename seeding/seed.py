from odo import odo, dshape
import pandas as pd
from config import seedcountrystring, seedcitystring

ds = dshape("var * {countryName: string, countryCode: string, countryID: int64}")
odo("anothersample.csv", pd.DataFrame, dshape=ds)
odo("anothersample.csv", seedcountrystring)

ds = dshape("var * {cityID: int64, cityName: string, cityCode: string, countryName: string}")
odo("world-cities.csv", pd.DataFrame, dshape=ds)
odo("world-cities.csv", seedcitystring)

