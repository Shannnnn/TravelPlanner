from flask_wtf import Form
from wtforms import StringField, DateField, FileField, SelectField, TextAreaField, ValidationError
from wtforms.validators import DataRequired
from model import Country, City, Trips

class TripForm(Form):
    trip_name = StringField('Trip Name', validators=[DataRequired()])
    trip_city = SelectField('City', validators=[DataRequired()], id="trip_city")
    trip_country = SelectField('Country', validators=[DataRequired()], id="trip_country")
    trip_date_from = DateField('From(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    trip_date_to = DateField('To(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
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
    trip_city = SelectField('City', validators=[DataRequired()], id="trip_city")
    trip_country = SelectField('Country', validators=[DataRequired()], id="trip_country")
    trip_date_from = DateField('From(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    trip_date_to = DateField('To(mm/dd/yyyy)', format='%m/%d/%Y', validators=[DataRequired()])
    trip_visibility = SelectField('Visibility', choices=[(0, 'Public'), (1, 'Private')], coerce=int)
    isFeatured = SelectField('Featured', choices=[(0,'No'),(1,'Yes')], coerce=int)

    def isPrivate(self, field):
        trips = Trips.query.all()
        if trips.visibility == 1:
            if trips.featuredTrip == 1:
                raise ValidationError("Private trip cannot be set to featured trips.")

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

    def check(self, field):
        if Country.query.filter_by(countryName=field.data).first():
            raise ValidationError('City already saved.')

class CityForm(Form):
    cityname = StringField('City', validators=[DataRequired()])
    citycode = StringField('Code', validators=[DataRequired()])

    def check(self, field):
        if City.query.filter_by(cityName=field.data).first():
            raise ValidationError('City already saved.')
