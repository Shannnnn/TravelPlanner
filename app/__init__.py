from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
db = SQLAlchemy(app)

from auth import model

bootstrap = Bootstrap(app)
app.config.from_object('config')
app.config['SECRET_KEY'] = 'flaskimplement'
<<<<<<< HEAD

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/travelplanner'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/travelplannerdb'
=======
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/travelplanner'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/travelplanner'
>>>>>>> fffd72dbed7140846c37ec8f3e936e032868cd94


from auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)

db.create_all()



app.debug = True


