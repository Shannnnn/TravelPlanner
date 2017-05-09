from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail

app = Flask(__name__)
db = SQLAlchemy(app)
mail=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'travelplannerSy@gmail.com'
app.config['MAIL_PASSWORD'] = 'viatorem'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail=Mail(app)

from auth import model
from trips import model

bootstrap = Bootstrap(app)
app.config.from_object('config')
app.config['SECRET_KEY'] = 'flaskimplement'



#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/travelplanner'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/travelplannerdb'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/travelplanner'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/travelplannerdb'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:imawesome@127.0.0.1:5432/travelplannerdb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:databaseadmin@127.0.0.1:5432/travelplannerdb'

from auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)

from trips.views import trip_blueprint
app.register_blueprint(trip_blueprint)

from landing.views import landing_blueprint
app.register_blueprint(landing_blueprint)

db.create_all()

app.debug = True



