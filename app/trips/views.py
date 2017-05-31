import os
from flask import Flask, render_template, redirect, Blueprint, request, url_for, flash, jsonify
from flask_login import current_user, login_required
from forms import TripForm, ItineraryForm, EditTripForm, EditItineraryForm
from model import Trips, Itineraries, itineraryLocationType, Country, City
from app.auth.model import Request
from app import db
from werkzeug import secure_filename
from app.auth.model import Photos
import datetime
from PIL import Image

trip = Flask(__name__)
trip_blueprint = Blueprint('trip_blueprint', __name__, template_folder='templates', url_prefix='/trips',
                           static_folder='static',
                           static_url_path='/static/')

img_folder = 'app/trips/static/images/trips/'
available_extension = set(['png', 'jpg', 'PNG', 'JPG'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in available_extension

@trip_blueprint.route('/createtrip', methods=['GET', 'POST'])
@login_required
def addtrip():
    error = None
    tripForm = TripForm()
    tripForm.trip_country.choices = [(a.countryName, a.countryName) for a in Country.query.all()]
    tripForm.trip_city.choices = [(a.cityName, a.cityName) for a in City.query.all()]
    if request.method == 'POST':
        if tripForm.validate_on_submit():
            now_loc = img_folder+str(current_user.id)
            #if directory is not yet created this function will create it
            if os.path.isdir(now_loc)==False:
                os.makedirs(now_loc)

            if tripForm.file.data and allowed_file(tripForm.file.data.filename):
                filename = secure_filename(tripForm.file.data.filename)
                tripForm.file.data.save(os.path.join(now_loc+'/', filename))
                uploadFolder = now_loc+'/'

                #the renaming process of the image
                nameNow = str(int(time.time()))+'.'+str(os.path.splitext(filename)[1][1:])

                #saving the changes
                os.rename(uploadFolder+filename, uploadFolder+nameNow)

                #this is the compressor part, this will optimize the image
                #and will decrease its file size but not losing that much quality
                img = Image.open(open(str(uploadFolder+nameNow), 'rb'))
                img.save(str(uploadFolder+nameNow), quality=90, optimize=True)

            tripform = Trips(tripName=tripForm.trip_name.data,
                             tripDateFrom=tripForm.trip_date_from.data,
                             tripDateTo=tripForm.trip_date_to.data,
                             userID=current_user.id,
                             tripCountry=tripForm.trip_country.data,
                             tripCity=tripForm.trip_city.data,
                             status=0,
                             visibility=tripForm.trip_visibility.data,
                             img_thumbnail=nameNow,
                             featuredTrip=0)
            db.session.add(tripform)
            db.session.commit()
            return redirect(url_for('trip_blueprint.trips'))


    ph = Photos.query.filter_by(id=current_user.profile_pic).first()
    if ph is None:
        cas = 'default'
    else:
        cas = ph.photoName

    return render_template('addtrip.html', form=tripForm, error=error, csID=str(current_user.id), csPic=str(cas))

@trip_blueprint.route('/', methods=['GET'])
@login_required
def trips():
    trip = Trips.query.filter_by(userID=current_user.id)
    return render_template('/trip.html', trips=trip, current_user=current_user)

@trip_blueprint.route('/<tripName>/edit', methods=['GET', 'POST'])
@login_required
def editTrips(tripName):
    tripname = Trips.query.filter_by(tripName=tripName).first()
    form = EditTripForm()
    form.trip_country.choices = [(a.countryName, a.countryName) for a in Country.query.all()]
    form.trip_city.choices = [(a.cityName, a.cityName) for a in City.query.all()]
    trips = Trips.query.all()
    if request.method == 'POST':
        if form.validate_on_submit():
            tripname.tripName = form.trip_name.data
            tripname.tripDateFrom = form.trip_date_from.data
            tripname.tripDateTo = form.trip_date_to.data
            tripname.tripCity = form.trip_city.data
            tripname.tripCountry = form.trip_country.data
            tripname.visibility = form.trip_visibility.data
            db.session.add(tripname)
            db.session.commit()
            return redirect(url_for("trip_blueprint.trips"))
        return render_template('trip.html', trips=trips)
    else:
        form.trip_name.data = tripname.tripName
        form.trip_date_from.data = tripname.tripDateFrom
        form.trip_date_to.data = tripname.tripDateTo
        form.trip_city.data = tripname.tripCity
        form.trip_country.data = tripname.tripCountry
        form.trip_visibility.data = tripname.visibility
    return render_template('edittrip.html', form=form, tripname=tripname)

@trip_blueprint.route('/<tripName>/additineraries', methods=['GET', 'POST'])
@login_required
def additineraries(tripName):
    tripid = Trips.query.filter_by(tripName=tripName).first()
    itineraryForm = ItineraryForm()
    itineraryForm.itinerary_location_type.choices = [(a.locationTypeID, a.locationType) for a in itineraryLocationType.query]
    if request.method == 'POST':
        if itineraryForm.validate_on_submit():
            itineraryform = Itineraries(itineraryName=itineraryForm.itinerary_name.data,
                             itineraryDate=itineraryForm.itinerary_date.data,
                             itineraryDesc=itineraryForm.itinerary_desc.data,
                             itineraryLocation=itineraryForm.itinerary_location.data,
                             itineraryTime=itineraryForm.itinerary_time.data,
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
@login_required
def itineraries(tripName):
    tripid = Trips.query.filter_by(tripName=tripName).first()
    itinerary = Itineraries.query.filter_by(tripID=tripid.tripID)
    trip = Trips.query.filter_by(userID=current_user.id, tripName=tripName).first()
    return render_template('itineraries.html', trip=trip, itineraries=itinerary)


@trip_blueprint.route('/<tripName>/itineraries/view', methods=['GET'])
@login_required
def itineraries_friends(tripName):
    tripid = Trips.query.filter_by(tripName=tripName).first()
    itinerary = Itineraries.query.filter_by(tripID=tripid.tripID)
    trip = Trips.query.filter_by(userID=current_user.id, tripName=tripName).first()
    return render_template('itineraries-friends.html', trip=trip, itineraries=itinerary)

@trip_blueprint.route('/<tripName>/<itineraryName>/edit', methods=['GET', 'POST'])
@login_required
def editItineraries(tripName, itineraryName):
    tripname = Trips.query.filter_by(tripName=tripName).first()
    itineraryname = Itineraries.query.filter_by(tripID=tripname.tripID, itineraryName=itineraryName).first()
    itineraries = Itineraries.query.all()
    form = EditItineraryForm()
    form.itinerary_location_type.choices = [(a.locationTypeID, a.locationType) for a in itineraryLocationType.query]
    if request.method == 'POST':
        if form.validate_on_submit():
            itineraryname.itineraryName = form.itinerary_name.data
            itineraryname.itineraryDate = form.itinerary_date.data
            itineraryname.itineraryDesc = form.itinerary_desc.data
            itineraryname.itineraryLocation = form.itinerary_location.data
            itineraryname.locationTypeID = form.itinerary_location_type.data
            itineraryname.itineraryTime = form.itinerary_time.data
            db.session.add(itineraryname)
            db.session.commit()
            return redirect(url_for("trip_blueprint.itineraries", tripName=tripName))
        return render_template('itineraries.html', trip=tripname, itineraries=itineraries)
    else:
        form.itinerary_name.data = itineraryname.itineraryName
        form.itinerary_date.data = itineraryname.itineraryDate
        form.itinerary_desc.data = itineraryname.itineraryDesc
        form.itinerary_location_type.data = itineraryname.locationTypeID
        form.itinerary_location.data = itineraryname.itineraryLocation
        form.itinerary_time.data = itineraryname.itineraryTime

    return render_template('edititineraries.html', form=form, tripname=tripname)

@trip_blueprint.route('/get_cities/')
def get_cities():
    countryName = request.args.get('country')
    cities = [(a.cityName, a.cityName) for a in City.query.filter_by(countryName=countryName).all()]
    return jsonify(cities)