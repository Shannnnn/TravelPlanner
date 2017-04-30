from flask_wtf import Form
from wtforms import StringField, PasswordField, ValidationError, DateField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from model import Trips

class TripForm(Form):
    trip_name = StringField('Trip Name', validators=[DataRequired()])
    trip_date_from = DateField('From(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    trip_date_to = DateField('To(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    file = FileField('Choose Thumbnail', validators=[DataRequired()])