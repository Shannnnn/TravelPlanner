from flask_wtf import Form
from wtforms import StringField, PasswordField, ValidationError, DateField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from model import Trips

class TripForm(Form):
    trip_name = StringField('Trip Name', validators=[DataRequired()])
    trip_date_from = DateField('From(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    trip_date_to = DateField('To(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    file = FileField('Choose Thumbnail', validators=[DataRequired()])

class ItineraryForm(Form):
    itinerary_name = StringField('Itinerary Name', validators=[DataRequired()])
    itinerary_date_from = DateField('From(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    itinerary_date_to = DateField('To(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    itinerary_desc = StringField('Description', validators=[DataRequired()])
    itinerary_time_from = StringField('From(hh:mm)', validators=[DataRequired()])
    itinerary_time_to = StringField('To(hh:mm)', validators=[DataRequired()])

class EditTripForm(Form):
    trip_name = StringField('Trip Name', validators=[DataRequired()])
    trip_date_from = DateField('From(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    trip_date_to = DateField('To(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])

class EditItineraryForm(Form):
    itinerary_name = StringField('Itinerary Name', validators=[DataRequired()])
    itinerary_date_from = DateField('From(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    itinerary_date_to = DateField('To(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    itinerary_desc = StringField('Description', validators=[DataRequired()])
    itinerary_time_from = StringField('From(hh:mm)', validators=[DataRequired()])
    itinerary_time_to = StringField('To(hh:mm)', validators=[DataRequired()])