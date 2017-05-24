from odo import odo, dshape
import pandas as pd
from config import seedcountrystring, seedcitystring, adminstring

# ds = dshape("var * {countryName: string, countryCode: string, countryID: int64}")
# odo("anothersample.csv", pd.DataFrame, dshape=ds)
# odo("anothersample.csv", seedcountrystring)
#
# ds = dshape("var * {cityID: int64, cityName: string, cityCode: string, countryName: string}")
# odo("world-cities.csv", pd.DataFrame, dshape=ds)
# odo("world-cities.csv", seedcitystring)

ds = dshape("var * {username: string, email: string, password: string, role_id: int64}")
odo("adminuser.csv", pd.DataFrame, dshap=ds)
odo("adminuser.csv", adminstring)
