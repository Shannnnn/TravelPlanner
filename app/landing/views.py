from flask import Flask, render_template, redirect, Blueprint, request, flash, url_for, jsonify, send_from_directory
from flask_login import current_user
from flask_login import LoginManager, current_user, AnonymousUserMixin
from app import db, app
from decorators import send_email, verify
from sqlalchemy import func, desc
from app.trips.model import Trips
from model import Anonymous

landing = Flask(__name__)
landing_blueprint = Blueprint('landing_blueprint', __name__, template_folder='templates', url_prefix='/main', static_folder='static', static_url_path='/static/')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous

POSTS_PER_PAGE = 4

@landing_blueprint.route('/')
@landing_blueprint.route('/index')
def index():
    label=verify()
    trips = Trips.query.order_by(desc(Trips.tripID)).paginate(1, POSTS_PER_PAGE, False)
    trips_for_most = Trips.query.order_by(Trips.tripID).paginate(1, POSTS_PER_PAGE, False)
    return render_template('index.html', title='TravelPlanner-Home', trips=trips, trips_m=trips_for_most, label=label)

@landing_blueprint.route('/view/<Tripname>', methods=['GET','POST'])
def mock(Tripname):
    trips = Trips.query.filter_by(tripName=Tripname).first()
    trips.viewsNum = trips.viewsNum + 1
    db.session.add(trips)
    db.session.commit()
    label = []
    label = verify()
    return render_template('view_trip.html', title=trips.tripName, trips=trips, label=label)

@landing_blueprint.route('/trip-plans/<linklabel>', methods=['GET','POST'])
def view_each(linklabel='all trips made in this site'):
    label=verify()
    til='Search Result'
    trips = db.session.query(Trips).filter(func.concat(Trips.tripName, ' ', Trips.tripDateFrom, ' ', Trips.tripDateTo).like('%'+linklabel+'%')).all()
    if linklabel=='most-popular':
        til='Most Popular'
        trips = Trips.query.order_by(Trips.tripID).limit(8).all()
        linklabel='Most Popular'
    elif linklabel=='newest-trip-plans':
        til='Newest Trips'
        trips = Trips.query.order_by(desc(Trips.tripID)).limit(8).all()
        linklabel='Newest Trip Plans'
    elif linklabel=='all trips made in this site':
        til='All Trips'
        trips = Trips.query.order_by(Trips.tripID).all()
        linklabel='All Trips'
    elif linklabel=='filtered_result':
        trip_ = []
        if request.args.get('option')=='all-trips':
            trips = Trips.query.order_by(Trips.tripID).all()
        elif request.args.get('option')=='most-popular':
            trips = Trips.query.order_by(Trips.tripID).all()
        elif request.args.get('option')=='newest-trip-plans':
            trips = Trips.query.order_by(desc(Trips.tripID)).all()

        for trip in trips:
            if (request.args.get('country') in trip.tripName) or (request.args.get('city') in trip.tripName):
                trip_.append(trip)
        return render_template('trip-plans.html', title=til, trips=trip_, label=label, search_label=request.args.get('city'))
    return render_template('trip-plans.html', title=til, trips=trips, label=label, search_label=linklabel)

@landing_blueprint.route('/paginate/<int:index>')
def paginate(index):
    tripnameL, fromL, toL, tripViews, image, determiner = [], [], [], [], [], True
    page_string = request.args.get('page')
    if int(page_string)==3:
        determiner=False
    if index==1:
        trips = Trips.query.order_by(desc(Trips.tripID)).paginate(int(page_string), POSTS_PER_PAGE, False)
    elif index==3 or index==2:
        trips = Trips.query.order_by(Trips.tripID).paginate(int(page_string), POSTS_PER_PAGE, False)

    for trip in trips.items:
        tripnameL.append(trip.tripName)
        fromL.append(trip.tripDateFrom)
        toL.append(trip.tripDateTo)
        tripViews.append(trip.viewsNum)
        image.append(trip.img_thumbnail)
  
    return jsonify(result1=tripnameL, result2=fromL, result3=toL, result4=tripViews, result5=image, size=len(tripnameL), determiner=determiner)

@landing_blueprint.route('/sendResponse')
def sendMail():
    body = "From: %s \n Email: %s \n Message: %s" % (request.args.get('name'), request.args.get('email'), request.args.get('body'))
    send_email('TravelPlanner', 'travelplannerSy@gmail.com', ['travelplannerSy@gmail.com'], body)
    return jsonify(sent=True)
