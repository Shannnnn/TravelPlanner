import os
from flask import Flask, render_template, redirect, Blueprint, request, jsonify, url_for, send_from_directory
from flask_login import current_user
from forms import TripForm, ItineraryForm, EditTripForm, EditItineraryForm
from model import Trips, Itineraries, itineraryLocationType, Country, City
from app import db
from werkzeug import secure_filename
from app.auth.model import Photos

trip = Flask(__name__)
trip_blueprint = Blueprint('trip_blueprint', __name__, template_folder='templates', url_prefix='/trips',
                           static_folder='static',
                           static_url_path='/static/')

img_folder = 'app/trips/static/images/'
available_extension = set(['png', 'jpg', 'PNG', 'JPG'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in available_extension

@trip_blueprint.route('/createtrip', methods=['GET', 'POST'])
def addtrip():
    global a
    error = None
    tripForm = TripForm()
    tripForm.trip_country.choices = [(a.countryID, a.countryName) for a in Country.query]
    tripForm.trip_city.choices = [(a.cityID, a.cityName) for a in City.query]
    if request.method == 'POST':
        if tripForm.validate_on_submit():
            tripform = Trips(tripName=tripForm.trip_name.data,
                             tripDateFrom=tripForm.trip_date_from.data,
                             tripDateTo=tripForm.trip_date_to.data,
                             userID=current_user.id,
                             tripCountry=tripForm.trip_country.data,
                             tripCity=tripForm.trip_city.data,
                             img_thumbnail=tripForm.file.data.filename)
            db.session.add(tripform)
            db.session.commit()

            if tripForm.file.data and allowed_file(tripForm.file.data.filename):
                filename = secure_filename(tripForm.file.data.filename)
                tripForm.file.data.save(os.path.join(img_folder+'trips/', filename))
            #ex = os.path.splitext(filename)[1][1:]
            #st = img_folder+'trips/'+filename
            #img = Image.open(open(str(st), 'rb'))
            #img.save(str(st), format=None, quality=50)

            return redirect(url_for('trip_blueprint.addtrip'))

    ph = Photos.query.filter_by(id=current_user.profile_pic).first()
    if ph is None:
        cas = 'default'
    else:
        cas = ph.photoName

    return render_template('addtrip.html', form=tripForm, error=error, csID=str(current_user.id), csPic=str(cas))

@trip_blueprint.route('/', methods=['GET'])
def trips():
    trip = Trips.query.filter_by(userID=current_user.id)
    return render_template('/trip.html', trips=trip, current_user=current_user)

@trip_blueprint.route('/<tripName>/edit', methods=['GET', 'POST'])
def editTrips(tripName):
    tripname = Trips.query.filter_by(tripName=tripName).first()
    form = EditTripForm()
    trips = Trips.query.all()
    if request.method == 'POST':
        if form.validate_on_submit():
            tripname.tripName = form.trip_name.data
            tripname.tripDateFrom = form.trip_date_from.data
            tripname.tripDateTo = form.trip_date_to.data
            db.session.add(tripname)
            db.session.commit()
            return redirect(url_for("trip_blueprint.trips"))
        return render_template('trip.html', trips=trips)
    else:
        form.trip_name.data = tripname.tripName
        form.trip_date_from.data = tripname.tripDateFrom
        form.trip_date_to.data = tripname.tripDateTo
    return render_template('edittrip.html', form=form, tripname=tripname)

@trip_blueprint.route('/<tripName>/additineraries', methods=['GET', 'POST'])
def additineraries(tripName):
    tripid = Trips.query.filter_by(tripName=tripName).first()
    itineraryForm = ItineraryForm()
    itineraryForm.itinerary_location_type.choices = [(a.locationTypeID, a.locationType) for a in itineraryLocationType.query]
    if request.method == 'POST':
        if itineraryForm.validate_on_submit():
            itineraryform = Itineraries(itineraryName=itineraryForm.itinerary_name.data,
                             itineraryDateFrom=itineraryForm.itinerary_date_from.data,
                             itineraryDateTo=itineraryForm.itinerary_date_to.data,
                             itineraryDesc=itineraryForm.itinerary_desc.data,
                             itineraryLocation=itineraryForm.itinerary_location.data,
                             itineraryTimeFrom=itineraryForm.itinerary_time_from.data,
                             itineraryTimeTo=itineraryForm.itinerary_time_to.data,
                             locationTypeID=itineraryForm.itinerary_location_type.data,
                             tripID=tripid.tripID)
            db.session.add(itineraryform)
            db.session.commit()
            return redirect(url_for("trip_blueprint.itineraries", tripName=tripName))

    ph = Photos.query.filter_by(id=current_user.profile_pic).first()
    if ph is None:
        cas = 'default'
    else:
        cas = ph.photoName

    return render_template('addItinerary.html', itineraries=itineraries, form=itineraryForm, csID=str(current_user.id), csPic=str(cas))

@trip_blueprint.route('/<tripName>/itineraries', methods=['GET'])
def itineraries(tripName):
    tripid = Trips.query.filter_by(tripName=tripName).first()
    itinerary = Itineraries.query.filter_by(tripID=tripid.tripID)
    itinerary2 = Itineraries.query.filter_by(tripID=tripid.tripID).first()
    itinerarylocationtype1 = itineraryLocationType.query.filter_by(locationTypeID=itinerary2.locationTypeID)
    trip = Trips.query.filter_by(userID=current_user.id, tripName=tripName).first()
    return render_template('itineraries.html', trip=trip, itineraryLocationType=itinerarylocationtype1, itineraries=itinerary)

@trip_blueprint.route('/<tripName>/<itineraryName>/edit', methods=['GET', 'POST'])
def editItineraries(tripName, itineraryName):
    tripname = Trips.query.filter_by(tripName=tripName).first()
    itineraryname = Itineraries.query.filter_by(tripID=tripname.tripID, itineraryName=itineraryName).first()
    itineraries = Itineraries.query.all()
    form = EditItineraryForm()
    form.itinerary_location_type.choices = [(a.locationTypeID, a.locationType) for a in itineraryLocationType.query]
    if request.method == 'POST':
        if form.validate_on_submit():
            itineraryname.itineraryName = form.itinerary_name.data
            itineraryname.itineraryDateFrom = form.itinerary_date_from.data
            itineraryname.itineraryDateTo = form.itinerary_date_to.data
            itineraryname.itineraryDesc = form.itinerary_desc.data
            itineraryname.itineraryLocation = form.itinerary_location.data
            itineraryname.locationTypeID = form.itinerary_location_type.data
            itineraryname.itineraryTimeFrom = form.itinerary_time_from.data
            itineraryname.itineraryTimeTo = form.itinerary_time_to.data
            db.session.add(itineraryname)
            db.session.commit()
            return redirect(url_for("trip_blueprint.itineraries", tripName=tripName))
        return render_template('itineraries.html', trip=tripname, itineraries=itineraries)
    else:
        form.itinerary_name.data = itineraryname.itineraryName
        form.itinerary_date_from.data = itineraryname.itineraryDateFrom
        form.itinerary_date_to.data = itineraryname.itineraryDateTo
        form.itinerary_desc.data = itineraryname.itineraryDesc
        form.itinerary_location_type.data = itineraryname.locationTypeID
        form.itinerary_location.data = itineraryname.itineraryLocation
        form.itinerary_time_from.data = itineraryname.itineraryTimeFrom
        form.itinerary_time_to.data = itineraryname.itineraryTimeTo
    return render_template('edititineraries.html', form=form, tripname=tripname)