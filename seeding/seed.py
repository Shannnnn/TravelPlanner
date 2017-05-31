from odo import odo, dshape
import pandas as pd
from config import seedcountrystring, seedcitystring, adminstring, itnloctypestring

# ds = dshape("var * {countryName: string, countryCode: string, countryID: int64}")
# odo("anothersample.csv", pd.DataFrame, dshape=ds)
# odo("anothersample.csv", seedcountrystring)
#
# ds = dshape("var * {cityID: int64, cityName: string, cityCode: string, countryName: string}")
# odo("world-cities.csv", pd.DataFrame, dshape=ds)
# odo("world-cities.csv", seedcitystring)

ds = dshape("var * {id: int64, username: string, email: string, password: string, role_id: int64, first_name: string, last_name: string, address: string, city: string, country: string, birth_date: string, contact_number: int64, description: string, profile_pic: int64, gender: string, first_login: string}")
odo("adminuser.csv", pd.DataFrame, dshape=ds)
odo("adminuser.csv", adminstring)

ds = dshape("var * {locationTypeID: int64, locationType: string, locationTypeIcon: string}")
odo("itnloctype.csv", pd.DataFrame, dshape=ds)
odo("itnloctype.csv", itnloctypestring)



#manual insertion
#COPY countries FROM '/anothersample.csv' DELIMITER ',' CSV HEADER;
#COPY cities FROM '/world-cities.csv' DELIMITER ',' CSV HEADER;