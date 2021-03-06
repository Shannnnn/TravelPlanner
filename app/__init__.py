from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import dbstring
from flask_compress import Compress


app = Flask(__name__)
db = SQLAlchemy(app)
mail = Mail(app)
Compress(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'travelplannerSy@gmail.com'
app.config['MAIL_PASSWORD'] = 'viatorem'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


app.config['SQLALCHEMY_DATABASE_URI'] = dbstring
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tkakffdbqitxpz:d06692592a1ccafca6ec426d1c8f13a5339cfb7792c6f757dc8dc6a3e0c8379d@ec2-23-21-235-142.compute-1.amazonaws.com:5432/df163mhfv9kda9'

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from auth import model
from trips import model

bootstrap = Bootstrap(app)
app.config.from_object('config')
app.config['SECRET_KEY'] = 'flaskimplement'

from auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)

from trips.views import trip_blueprint
app.register_blueprint(trip_blueprint)

from landing.views import landing_blueprint
app.register_blueprint(landing_blueprint)


db.create_all()

app.debug = True