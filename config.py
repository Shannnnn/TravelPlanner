from flask import Flask
import os

_basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

<<<<<<< HEAD
dbstring = 'postgresql://postgres:imawesome@127.0.0.1:5432/travelplannerdb'
seedcountrystring = 'postgresql://postgres:@127.0.0.1:5432/travelplannerdb::countries'
seedcitystring = 'postgresql://postgres:@127.0.0.1:5432/travelplannerdb::cities'
=======
dbstring = 'postgresql://postgres:databaseadmin@127.0.0.1:5432/travelplannerdb'
seedcountrystring = 'postgresql://postgres:databaseadmin@127.0.0.1:5432/travelplannerdb::countries'
seedcitystring = 'postgresql://postgres:databaseadmin@127.0.0.1:5432/travelplannerdb::cities'
>>>>>>> b4334494364de534057b25a2c2519c98f949d185

adminstring = 'postgresql://postgres:databaseadmin@127.0.0.1:5432/travelplannerdb::users'
itnloctypestring = 'postgresql://postgres:databaseadmin@127.0.0.1:5432/travelplannerdb::itinerarylocationtype'
