from flask_wtf import Form
from wtforms import StringField, DateField, FileField, SelectField, TextAreaField
from wtforms.validators import DataRequired

class TripForm(Form):
    trip_name = StringField('Trip Name', validators=[DataRequired()])
    trip_city = SelectField('City', choices=[])
    trip_country = SelectField('Country', choices=[])
    trip_date_from = DateField('From(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    trip_date_to = DateField('To(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    file = FileField('Choose Thumbnail', validators=[DataRequired()])

class ItineraryForm(Form):
    itinerary_name = StringField('Itinerary Name', validators=[DataRequired()])
    itinerary_date_from = DateField('From(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    itinerary_date_to = DateField('To(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    itinerary_desc = TextAreaField('Description', validators=[DataRequired()])
    itinerary_location = StringField('Location', validators=[DataRequired()])
    itinerary_location_type = SelectField('Type', choices=[], coerce=int)
    itinerary_time_from = StringField('From(hh:mm)', validators=[DataRequired()])
    itinerary_time_to = StringField('To(hh:mm)', validators=[DataRequired()])

class EditTripForm(Form):
    trip_name = StringField('Trip Name', validators=[DataRequired()])
    trip_location = SelectField('Location', choices=[])
    trip_date_from = DateField('From(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    trip_date_to = DateField('To(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])

class EditItineraryForm(Form):
    itinerary_name = StringField('Itinerary Name', validators=[DataRequired()])
    itinerary_date_from = DateField('From(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    itinerary_date_to = DateField('To(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    itinerary_desc = StringField('Description', validators=[DataRequired()])
    itinerary_location = StringField('Location', validators=[DataRequired()])
    itinerary_location_type = SelectField('Type', choices=[], coerce=int)
    itinerary_time_from = StringField('From(hh:mm)', validators=[DataRequired()])
    itinerary_time_to = StringField('To(hh:mm)', validators=[DataRequired()])