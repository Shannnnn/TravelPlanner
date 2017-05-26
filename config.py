from flask import Flask
import os

_basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

dbstring = 'postgresql://postgres:databaseadmin@127.0.0.1:5432/travelplannerdb'
seedcountrystring = 'postgresql://postgres:databaseadmin@127.0.0.1:5432/travelplannerdb::countries'
seedcitystring = 'postgresql://postgres:databaseadmin@127.0.0.1:5432/travelplannerdb::cities'
<<<<<<< HEAD
=======
adminstring = 'postgresql://postgres:databaseadmin@127.0.0.1:5432/travelplannerdb::users'
itnloctypestring = 'postgresql://postgres:databaseadmin@127.0.0.1:5432/travelplannerdb::itinerarylocationtype'
>>>>>>> fc119c29104da64c99b1f6f6bacd55b8eede9158
