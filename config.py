from flask import Flask
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

<<<<<<< HEAD
dbstring = 'postgresql://postgres:imawesome@127.0.0.1:5432/travelplannerdb'
=======
app = Flask(__name__)

dbstring = 'postgresql://postgres:databaseadmin@127.0.0.1:5432/travelplannerdb'
seedcountrystring = 'postgresql://postgres:databaseadmin@127.0.0.1:5432/travelplannerdb::countries'
seedcitystring = 'postgresql://postgres:databaseadmin@127.0.0.1:5432/travelplannerdb::cities'

>>>>>>> Trips
