from flask_wtf import Form
from wtforms import StringField, DateField, FileField, SelectField, TextAreaField
from wtforms.validators import DataRequired

class TripForm(Form):
    trip_name = StringField('Trip Name', validators=[DataRequired()])
    trip_city = SelectField('City', choices=[])
    trip_country = SelectField('Country', choices=[])
    trip_date_from = DateField('From(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    trip_date_to = DateField('To(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    trip_status = SelectField('Status', choices=[(0,'Inactive'),(1,'Active')], coerce=int)
    trip_visibility = SelectField('Visibility', choices=[(0,'Public'),(1,'Private')], coerce=int)
    file = FileField('Choose Thumbnail', validators=[DataRequired()])

class ItineraryForm(Form):
    itinerary_name = StringField('Itinerary Name', validators=[DataRequired()])
    itinerary_date = DateField('Date(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    itinerary_desc = TextAreaField('Description', validators=[DataRequired()])
    itinerary_location = StringField('Location', validators=[DataRequired()])
    itinerary_location_type = SelectField('Type', choices=[], coerce=int)
    itinerary_time = StringField('Time(hh:mm)', validators=[DataRequired()])

class EditTripForm(Form):
    trip_name = StringField('Trip Name', validators=[DataRequired()])
    trip_city = SelectField('City', choices=[])
    trip_country = SelectField('Country', choices=[])
    trip_date_from = DateField('From(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    trip_date_to = DateField('To(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    trip_status = SelectField('Status', choices=[(0, 'Inactive'), (1, 'Active')], coerce=int)
    trip_visibility = SelectField('Visibility', choices=[(0, 'Public'), (1, 'Private')], coerce=int)

class EditItineraryForm(Form):
    itinerary_name = StringField('Itinerary Name', validators=[DataRequired()])
    itinerary_date = DateField('Date(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    itinerary_desc = TextAreaField('Description', validators=[DataRequired()])
    itinerary_location = StringField('Location', validators=[DataRequired()])
    itinerary_location_type = SelectField('Type', choices=[], coerce=int)
    itinerary_time = StringField('Time(hh:mm)', validators=[DataRequired()])

class CountryForm(Form):
    countryname= StringField('Country', validators=[DataRequired()])
    countrycode = StringField('Code', validators=[DataRequired()])

class CityForm(Form):
    cityname = StringField('City', validators=[DataRequired()])
    citycode = StringField('Code', validators=[DataRequired()])
