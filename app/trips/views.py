import os
from flask import Flask, render_template, redirect, Blueprint, request, flash, url_for, send_from_directory
from flask_login import current_user
from forms import TripForm, ItineraryForm, EditTripForm
from model import Trips, Itineraries
from app import db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from werkzeug import secure_filename
from PIL import Image
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
    error = None
    tripForm = TripForm()
    if request.method == 'POST':
        if tripForm.validate_on_submit():
            tripform = Trips(tripName=tripForm.trip_name.data,
                             tripDateFrom=tripForm.trip_date_from.data,
                             tripDateTo=tripForm.trip_date_to.data,
                             userID=current_user.id,
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
    return render_template('/trip.html', trips=trip)

@trip_blueprint.route('/<tripName>/edit', methods=['GET', 'POST'])
def editTrips(tripName):
    tripname = Trips.query.filter_by(tripName=tripName).first()
    form = EditTripForm()
    trips = Trips.query.all()
    if request.method == 'POST':
        if form.validate_on_submit():
            form = Itineraries(tripName=form.trip_name.data,
                               tripDateFrom=form.trip_date_from.data,
                               tripDateTo=form.trip_date_to.data)
            db.session.add(form)
            db.session.commit()
        return render_template('trip.html', trips=trips)
    else:
        form.trip_name.data = tripname.tripName
        form.trip_date_from.data = tripname.tripDateFrom
        form.trip_date_to.data = tripname.tripDateTo
    return render_template('edittrip.html', form=form, tripname=tripname)

@trip_blueprint.route('/<tripName>/additineraries', methods=['GET', 'POST'])
def additineraries(tripName):
    tripid = Trips.query.filter_by(tripName=tripName).first()
    error = None
    itineraryForm = ItineraryForm()
    if request.method == 'POST':
        if itineraryForm.validate_on_submit():
            itineraryform = Itineraries(itineraryName=itineraryForm.itinerary_name.data,
                             itineraryDateFrom=itineraryForm.itinerary_date_from.data,
                             itineraryDateTo=itineraryForm.itinerary_date_to.data,
                             itineraryDesc=itineraryForm.itinerary_desc.data,
                             itineraryTimeFrom=itineraryForm.itinerary_time_from.data,
                             itineraryTimeTo=itineraryForm.itinerary_time_to.data,
                             tripID=tripid.tripID)
            db.session.add(itineraryform)
            db.session.commit()
            return redirect(url_for("trip_blueprint.additineraries", tripName=tripName))

    ph = Photos.query.filter_by(id=current_user.profile_pic).first()
    if ph is None:
        cas = 'default'
    else:
        cas = ph.photoName

    return render_template('addItinerary.html', error=error, itineraries=itineraries, form=itineraryForm, csID=str(current_user.id), csPic=str(cas))

@trip_blueprint.route('/<tripName>/itineraries', methods=['GET'])
def itineraries(tripName):
    tripid = Trips.query.filter_by(tripName=tripName).first()
    itinerary = Itineraries.query.filter_by(tripID=tripid.tripID)
    trip = Trips.query.filter_by(userID=current_user.id)
    return render_template('itineraries.html', trips=trip, itineraries=itinerary)
