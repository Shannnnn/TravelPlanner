from flask import Flask, render_template, redirect, Blueprint, request, flash, url_for, jsonify, send_from_directory
from flask_login import current_user
from flask_login import LoginManager, current_user, AnonymousUserMixin
from app import db, app
from decorators import send_email, verify, POSTS_PER_PAGE, maxNum, maxPage, max_for_most, max_for_new
from sqlalchemy import func, desc
from app.trips.model import Trips, Itineraries
from app.auth.model import User, Photos
from model import Anonymous

landing = Flask(__name__)
landing_blueprint = Blueprint('landing_blueprint', __name__, template_folder='templates', url_prefix='/main', static_folder='static', static_url_path='/static/')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous

#helper functions
def return_res_for_pic(user):
    photo = ""
    ph = Photos.query.filter_by(id=user.profile_pic).first()
    if ph is None:
        photo = "default"
    else:
        photo = str(ph.photoName)
    return photo

def determine_pic(users, counter):
    user_photos = []
    if counter==0:
        user_photos.append(return_res_for_pic(users))
    else:
        for r in users:
            user_photos.append(return_res_for_pic(r))
    return user_photos

def trip_query_1(num):
    trips = Trips.query.order_by(desc(Trips.tripID)).paginate(num, POSTS_PER_PAGE, False)
    return trips

def trip_query_2(num):
    return Trips.query.filter(Trips.viewsNum>maxNum).paginate(num, POSTS_PER_PAGE, False)

def trip_query_3(var):
    return db.session.query(Trips).filter(func.concat(Trips.tripName, ' ', Trips.tripDateFrom, ' ', Trips.tripDateTo).like('%'+var+'%')).all()

def user_query_1(var):
    return db.session.query(User).filter(func.concat(User.username, ' ', User.first_name, ' ', User.last_name).like('%'+var+'%')).all()

def til_(n):
    l = ['Most Popular', 'Newest Trips', 'All Trips']
    return l[n]

def trip_query_mod(n):
    if n==0:
        trips = Trips.query.filter(Trips.viewsNum>maxNum).limit(max_for_most).all()
    elif n==1:
        trips = Trips.query.order_by(desc(Trips.tripID)).limit(max_for_new).all()
    elif n==2:
        trips = Trips.query.order_by(Trips.tripID).all()
    return trips


#routes
@landing_blueprint.route('/')
@landing_blueprint.route('/index')
def index():
    return render_template('index.html', title='TravelPlanner-Home', trips=trip_query_1(1), trips_m=trip_query_2(1), label=verify())

@landing_blueprint.route('/about')
@landing_blueprint.route('/about/')
def about():
    return render_template('about.html', title='About', label=verify())

@landing_blueprint.route('/response')
@landing_blueprint.route('/response/')
def sendUs():
    return render_template('response.html', title='Response', label=verify())

@landing_blueprint.route('/siteSearch', methods=['GET','POST'])
def siteSearch():
    return render_template('search.html', title='Search Result', label=verify(), trips=trip_query_3(request.args.get('search_1')), users=user_query_1(request.args.get('search_1')), ph_1=determine_pic(user_query_1(request.args.get('search_1')),1))

@landing_blueprint.route('/view/<Tripname>', methods=['GET','POST'])
def mock(Tripname):
    trips = Trips.query.filter_by(tripName=Tripname).first()
    trips.viewsNum = trips.viewsNum + 1

    user =User.query.filter_by(id=trips.userID).first() 

    itern = Itineraries.query.filter_by(tripID=trips.tripID).all()

    all_trips = Trips.query.filter_by(userID=user.id).all()

    db.session.add(trips)
    db.session.commit()
    return render_template('view_trip.html', title=trips.tripName, trips=trips, label=verify(), ite=itern, user=user, ph_1=determine_pic(user,0), suggestedTrips=all_trips)

@landing_blueprint.route('/trip-plans/')
@landing_blueprint.route('/trip-plans/<linklabel>', methods=['GET','POST'])
def view_each(linklabel='all trips made in this site'):
    til=linklabel
    trips = trip_query_3(linklabel)

    lbl = ['most-popular','newest-trip-plans','all trips made in this site']
    if linklabel in lbl:
        for index, r in enumerate(lbl):
            if linklabel==r:
                til = til_(index)
                trips = trip_query_mod(index)

    elif linklabel=='filtered_result':
        trip_ = []
        for index_1, r_1 in enumerate(lbl):
            if request.args.get('option')==r_1:
                trips = trip_query_mod(index_1)

        for trip in trips:
            if (request.args.get('country') in trip.tripName) or (request.args.get('city') in trip.tripName):
                trip_.append(trip)
        return render_template('trip-plans.html', title=til, trips=trip_, label=verify(), search_label=request.args.get('city'))
    return render_template('trip-plans.html', title=til, trips=trips, label=verify(), search_label=til)

@landing_blueprint.route('/paginate/<int:index>')
def paginate(index):
    tripnameL, fromL, toL, tripViews, image = ([] for i in range(5))
    determiner = True
    page_string = request.args.get('page')
    if int(page_string)==maxPage:
        determiner=False
    if index==1:
        trips = trip_query_1(int(page_string))
    elif index==3 or index==2:
        trips = trip_query_2(int(page_string))

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
