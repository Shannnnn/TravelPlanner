import os  # main
from flask import Flask, render_template, redirect, Blueprint, request, flash, url_for, session, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, AnonymousUserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from model import User, Role, Anonymous, Photos, Connection, Photos, Request
from forms import LoginForm, RegisterForm, EditForm, SearchForm, PasswordSettingsForm, EmailResetForm, PasswordResetForm
from app import db, app
from decorators import required_roles, get_friends, get_friend_requests, allowed_file, deleteTrip_user, img_folder, get_edit_friends
from decorators import is_permitted_or_pending, is_permitted_or_pending2, is_friends_or_pending, is_friends_or_pending2, user_query, get_edit_requests
from app.landing.views import landing_blueprint
from werkzeug import secure_filename
from PIL import Image
from app.trips.model import Trips, Itineraries, Country, City, itineraryLocationType
from app.trips.forms import EditTripForm, EditItineraryForm, TripForm, CountryForm, CityForm, ItineraryForm, AdminEditTripForm
import datetime
import time
from sqlalchemy import func, desc
from app.landing.decorators import send_email

auth = Flask(__name__)
auth_blueprint = Blueprint('auth_blueprint', __name__, template_folder='templates', static_folder='static',
                           static_url_path='/static/')

img_folder = 'app/auth/static/images/users/'
available_extension = set(['png', 'jpg', 'PNG', 'JPG'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in available_extension

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_blueprint.login'
login_manager.anonymous_user = Anonymous

POSTS_PER_PAGE = 10
TRIPS_PER_PAGE = 12


def filter_user_for_admin(roleid):
    return User.query.filter_by(role_id=roleid)

def pageFormula(total, perpage):
    if total % perpage == 0:
        return total / perpage
    return (total / perpage) + 1

# to get the user profile pictures easily
def get_profile(profileString):
    ph = Photos.query.filter_by(id=profileString).first()
    if ph is None:
        return 'default'
    return ph.photoName

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --------> START ADMIN
@auth_blueprint.route('/admin')
@login_required
@required_roles('Admin')
def addash():
    users = User.query.all()
    trips = Trips.query.all()
    countries = Country.query.all()
    cities = City.query.all()
    return render_template('admin/admindashboard.html', users=users, trips=trips, countries=countries, cities=cities)

@auth_blueprint.route('/admin/settings/<username>', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def settings(username):
    form = PasswordSettingsForm()
    user = User.query.filter_by(username=username).first()
    if request.method == 'POST':
        if form.validate_on_submit():
            if check_password_hash(current_user.password, request.form['currpassword']):
                current_user.password = generate_password_hash(form.newpassword.data)
                db.session.add(current_user)
                db.session.commit()
                flash('Changes saved!')
                result = User.query.all()
                return render_template('admin/users.html', form=form, result=result, numm=len(result))
            else:
                flash('Incorrect Password!')
                return render_template('admin/settings.html', form=form, user=user)
        else:
            form.newpassword.data = current_user.password
            return render_template('admin/settings.html', form=form, user=user)
    return render_template('admin/settings.html', form=form, user=user)

@auth_blueprint.route('/admin/paginate/users/<condition>')
@login_required
@required_roles('Admin')
def paginate_users(condition):
    uid, uname, uemail, ufname, ulname, uroleId = ([] for i in range(6))
    pageNumber = request.args.get('page')

    result = User.query.order_by(User.id).paginate(int(pageNumber), POSTS_PER_PAGE, False)

    if int(condition) == 0:
        pass
    else:
        result = filter_user_for_admin(condition).paginate(int(pageNumber), POSTS_PER_PAGE, False)

    for user in result.items:
        uid.append(user.id)
        uname.append(user.username)
        uemail.append(user.email)
        ufname.append(user.first_name)
        ulname.append(user.last_name)
        if user.role_id == 1:
            uroleId.append('Admin')
        elif user.role_id == 2:
            uroleId.append('Moderator')
        elif user.role_id == 3:
            uroleId.append('Member')

    return jsonify(u_id=uid, u_name=uname, u_email=uemail, u_fname=ufname, u_lname=ulname, u_role=uroleId,
                   size=len(uid))

@auth_blueprint.route('/admin/users/sort/admin', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def sortadmin():
    result = User.query.filter_by(role_id='1').paginate(1, POSTS_PER_PAGE, False)
    return render_template('admin/users.html', result=result, stry=1,
                       numm=pageFormula(User.query.filter_by(role_id='1').count(), POSTS_PER_PAGE))

@auth_blueprint.route('/admin/users/sort/moderator', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def sortmod():
    result = User.query.filter_by(role_id='2').paginate(1, POSTS_PER_PAGE, False)
    return render_template('admin/users.html', result=result, stry=2,
                       numm=pageFormula(User.query.filter_by(role_id='2').count(), POSTS_PER_PAGE))

@auth_blueprint.route('/admin/users/sort/member', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def sortuser():
    result = User.query.filter_by(role_id='3').paginate(1, POSTS_PER_PAGE, False)
    return render_template('admin/users.html', result=result, stry=3,
                       numm=pageFormula(User.query.filter_by(role_id='3').count(), POSTS_PER_PAGE))


# USERS --> read
@auth_blueprint.route('/admin/users', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def manageusers():
    result = User.query.order_by(User.id).paginate(1, POSTS_PER_PAGE, False)
    return render_template('admin/users.html', result=result, stry=0,
                           numm=pageFormula(User.query.order_by(User.id).count(), POSTS_PER_PAGE))

@auth_blueprint.route('/admin/users/create', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def addusers():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(username=form.username.data,
                        email = form.email.data,
                        password = form.password.data,
                        role_id = '3')
            db.session.add(user)
            db.session.commit()
            flash("Your changes have been saved.")
            result = User.query.order_by(User.id).paginate(1, POSTS_PER_PAGE, False)
            return render_template('admin/users.html', result=result, stry=0,
                           numm=pageFormula(User.query.order_by(User.id).count(), POSTS_PER_PAGE))
    return render_template('admin/createusers.html', form=form)

# update
@auth_blueprint.route('/admin/users/edit/<username>', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def editusers(username):
    user = User.query.filter_by(username=username).first()
    form = EditForm()
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.address = form.address.data
        user.city = form.city.data
        user.country = form.country.data
        user.birth_date = form.birth_date.data
        user.contact_num = form.contact_num.data
        user.description = form.description.data
        user.gender = form.gender.data
        now_loc = img_folder + str(user.id)
        if os.path.isdir(now_loc) == False:
            os.makedirs(now_loc)

        if form.file.data.filename == None or form.file.data.filename == '':
            user.profile_pic = user.profile_pic
        else:
            if form.file.data and allowed_file(form.file.data.filename):
                filename = secure_filename(form.file.data.filename)
                form.file.data.save(os.path.join(now_loc + '/', filename))

                uploadFolder = now_loc + '/'
                nameNow = str(int(time.time())) + '.' + str(os.path.splitext(filename)[1][1:])
                os.rename(uploadFolder + filename, uploadFolder + nameNow)

            date = datetime.datetime.today().strftime('%m/%d/%y')
            photo = Photos(photoName=nameNow, photoDate=date, photoLocation=now_loc, userID=user.id)
            db.session.add(photo)
            db.session.commit()

            ph_1 = Photos.query.filter_by(userID=user.id).all()
            for p in ph_1:
                if p.photoName == str(nameNow):
                    user.profile_pic = p.id

        db.session.add(user)
        db.session.commit()

        ph = Photos.query.filter_by(id=user.profile_pic).first()
        if ph is None:
            cas = 'default'
        else:
            cas = ph.photoName

        flash("Your changes have been saved.")
        result = User.query.order_by(User.id).paginate(1, POSTS_PER_PAGE, False)
        return render_template('admin/users.html', result=result, stry=0,
                               numm=pageFormula(User.query.order_by(User.id).count(), POSTS_PER_PAGE))
    else:
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.address.data = user.address
        form.city.data = user.city
        form.country.data = user.country
        form.birth_date.data = user.birth_date
        form.contact_num.data = user.contact_num
        form.description.data = user.description
        form.gender.data = user.gender

        ph = Photos.query.filter_by(id=user.profile_pic).first()
        if ph is None:
            cas = 'default'
        else:
            cas = ph.photoName
        return render_template('admin/editusers.html', user=user, form=form, csID=str(user.id),
                               csPic=str(cas))

 # delete
@auth_blueprint.route('/admin/users/remove/<username>', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def deleteusers(username):
    user = User.query.filter_by(username=username).first()
    photo = Photos.query.filter_by(userID = user.id).delete()
    deleteTrip_user(user.id)
    #if user.profile_pic != 'default':
    #    os.remove(img_folder + str(user.profile_pic))
    db.session.delete(user)
    db.session.commit()
    result = User.query.order_by(User.id).paginate(1, POSTS_PER_PAGE, False)
    return render_template('admin/users.html', result=result, stry=0,
                           numm=pageFormula(User.query.order_by(User.id).count(), POSTS_PER_PAGE))

# TRIPS --> read
@auth_blueprint.route('/admin/paginate/trips')
@login_required
@required_roles('Admin')
def paginate_trip():
    tname, tfrom, tto, tviews = ([] for i in range(4))
    pageNumber = request.args.get('page')

    result = Trips.query.order_by(Trips.tripID).paginate(int(pageNumber), TRIPS_PER_PAGE, False)

    for trip in result.items:
        tname.append(trip.tripName)
        tfrom.append(trip.tripDateFrom)
        tto.append(trip.tripDateTo)
        tviews.append(trip.viewsNum)

    return jsonify(t_name=tname, t_from=tfrom, t_to=tto, t_views=tviews, size=len(tname))

# TRIPS --> read
@auth_blueprint.route('/admin/trips')
@login_required
@required_roles('Admin')
def managetrips():
    result = Trips.query.order_by(Trips.tripID).paginate(1, TRIPS_PER_PAGE, False)
    return render_template('admin/trips.html', result=result, numm=pageFormula(len(Trips.query.all()), TRIPS_PER_PAGE))

@auth_blueprint.route('/admin/trips/add', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
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
            result = Trips.query.order_by(Trips.tripID).paginate(1, TRIPS_PER_PAGE, False)
            return render_template('admin/trips.html', result=result,
                                   numm=pageFormula(len(Trips.query.all()), TRIPS_PER_PAGE))


    ph = Photos.query.filter_by(id=current_user.profile_pic).first()
    if ph is None:
        cas = 'default'
    else:
        cas = ph.photoName

    return render_template('/admin/addtrips.html', form=tripForm, error=error, csID=str(current_user.id), csPic=str(cas))

# delete
@auth_blueprint.route('/admin/trips/remove/<tripName>', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def removetrips(tripName):
    trips = Trips.query.filter_by(tripName=tripName).first()
    Itineraries.query.filter_by(tripID = trips.tripID).delete()
    os.remove('app/trips/static/images/trips/'+str(trips.userID)+'/'+trips.img_thumbnail)
    db.session.delete(trips)
    db.session.commit()
    result = Trips.query.order_by(Trips.tripID).paginate(1, TRIPS_PER_PAGE, False)
    return render_template('admin/trips.html', result=result, numm=pageFormula(len(Trips.query.all()), TRIPS_PER_PAGE))

# update
@auth_blueprint.route('/admin/trips/edit/<tripName>', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def editTrips(tripName):
    tripname = Trips.query.filter_by(tripName=tripName).first()
    form = AdminEditTripForm()
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
            tripname.featuredTrip = form.isFeatured.data
            db.session.add(tripname)
            db.session.commit()
            result = Trips.query.order_by(Trips.tripID).paginate(1, TRIPS_PER_PAGE, False)
            return render_template('admin/trips.html', result=result,
                                   numm=pageFormula(len(Trips.query.all()), TRIPS_PER_PAGE))
    else:
        form.trip_name.data = tripname.tripName
        form.trip_date_from.data = tripname.tripDateFrom
        form.trip_date_to.data = tripname.tripDateTo
        form.trip_city.data = tripname.tripCity
        form.trip_country.data = tripname.tripCountry
        form.trip_visibility.data = tripname.visibility
        form.isFeatured.data = tripname.featuredTrip
    return render_template('/admin/edittrips.html', form=form, tripname=tripname)

@auth_blueprint.route('/admin/trips/<tripName>/itineraries', methods=['GET'])
@login_required
@required_roles('Admin')
def itineraries(tripName):
    tripid = Trips.query.filter_by(tripName=tripName).first()
    itinerary = Itineraries.query.filter_by(tripID=tripid.tripID)
    trip = Trips.query.filter_by(userID=current_user.id, tripName=tripName).first()
    return render_template('/admin/itineraries.html', trip=trip, itineraries=itinerary, tripName=tripName)

@auth_blueprint.route('/admin/trips/<tripName>/additineraries', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
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
            return redirect(url_for("auth_blueprint.itineraries", tripName=tripName))

    ph = Photos.query.filter_by(id=current_user.profile_pic).first()
    if ph is None:
        cas = 'default'
    else:
        cas = ph.photoName

    return render_template('/admin/additineraries.html', itineraries=itineraries, form=itineraryForm, csID=str(current_user.id), csPic=str(cas))

@auth_blueprint.route('/admin/trips/<tripName>/<itineraryName>/edit', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
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
            return redirect(url_for("auth_blueprint.itineraries", tripName=tripName))
        return render_template('admin/itineraries.html', trip=tripname, itineraries=itineraries)
    else:
        form.itinerary_name.data = itineraryname.itineraryName
        form.itinerary_date.data = itineraryname.itineraryDate
        form.itinerary_desc.data = itineraryname.itineraryDesc
        form.itinerary_location_type.data = itineraryname.locationTypeID
        form.itinerary_location.data = itineraryname.itineraryLocation
        form.itinerary_time.data = itineraryname.itineraryTime
    return render_template('admin/edititinerary.html', form=form, trip=tripname)

@auth_blueprint.route('/paginate/trips/location')
@login_required
@required_roles('Admin')
def paginate_location_for_admin():
    cnName, cnCode, cnID = [],[],[]
    country = Country.query.order_by(Country.countryName).paginate(int(request.args.get('page')), 11, False)
    for c in country.items:
        cnName.append(c.countryName)
        cnID.append(c.countryID)
        cnCode.append(c.countryCode)
    return jsonify(cnName=cnName, cnID=cnID, cnCode=cnCode, size=len(cnName))

@auth_blueprint.route('/admin/trips/location')
@login_required
@required_roles('Admin')
def locations():
    country = Country.query.order_by(Country.countryName).paginate(1, 11, False)
    cc = len(Country.query.order_by(Country.countryName).all())
    return render_template('/admin/locations.html', country=country, stry=pageFormula(cc, 11))

@auth_blueprint.route('/admin/trips/location/new', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def addlocations():
    form = CountryForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            country = Country(countryName=form.countryname.data, countryCode=form.countrycode.data)
            db.session.add(country)
            db.session.commit()
            return redirect(url_for("auth_blueprint.locations"))
    return render_template('/admin/editlocations.html', form=form)

@auth_blueprint.route('/admin/trips/location/remove/<countryID>', methods=['GET','POST'])
@login_required
@required_roles('Admin')
def removelocations(countryID):
    country = Country.query.filter_by(countryID=countryID).first()
    City.query.filter_by(countryName= country.countryName).delete()
    db.session.delete(country)
    db.session.commit()
    return redirect(url_for("auth_blueprint.locations"))

@auth_blueprint.route('/admin/trips/location/edit/<countryID>', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def editlocations(countryID):
    country = Country.query.filter_by(countryID = countryID).first()
    form = CountryForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            country.countryName = form.countryname.data
            country.countryCode = form.countrycode.data
            db.session.add(country)
            db.session.commit()
            return redirect(url_for("auth_blueprint.locations"))
    else:
        form.countryname.data = country.countryName
        form.countrycode.data = country.countryCode
    return render_template('/admin/editlocations.html', form=form, countries=country)

@auth_blueprint.route('/paginate/trips/location/cities/<countryName>')
@login_required
@required_roles('Admin')
def paginate_location_cities_for_admin(country):
    ctName, ctCode, ctID, cnName_ = [],[],[], []
    city = City.query.filter_by(countryName=country).paginate(int(request.args.get('page')), 10, False)
    for c in city.items:
        ctName.append(c.cityName)
        ctID.append(c.cityID)
        ctCode.append(c.cityCode)
    return jsonify(ctName=ctName, ctID=ctID, ctCode=ctCode, cnName_=country, size=len(ctName))

@auth_blueprint.route('/admin/trips/<countryID>/city')
@login_required
@required_roles('Admin')
def cities(countryID):
    city = City.query.filter_by(countryID=countryID).paginate(1, 10, False)
    clenght = len(City.query.filter_by(countryID=countryID).all())
    country = Country.query.filter_by(countryID = countryID).first()
    return render_template('/admin/cities.html', city=city, country=country, stry=pageFormula(clenght, 10))

@auth_blueprint.route('/admin/trips/<countryID>/city/add', methods=['POST', 'GET'])
@login_required
@required_roles('Admin')
def addcities(countryID):
    country = Country.query.filter_by(countryID=countryID).first()
    form = CityForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            cities = City(cityName=form.cityname.data,
                          cityCode=form.citycode.data,
                          countryID=countryID)
            db.session.add(cities)
            db.session.commit()
            return redirect(url_for("auth_blueprint.cities", countryID=countryID))
    else:
        return render_template('/admin/editcities.html', form=form, country=country)

@auth_blueprint.route('/admin/trips/<countryID>/city/<cityID>/edit', methods=['POST', 'GET'])
@login_required
@required_roles('Admin')
def editcities(cityID, countryID):
    country = Country.query.filter_by(countryID=countryID).first()
    form = CityForm()
    city = City.query.filter_by(cityID=cityID).first()
    if request.method == 'POST':
        if form.validate_on_submit():
            city.cityName = form.cityname.data
            city.cityCode = form.citycode.data
            city.countryID = countryID
            db.session.add(city)
            db.session.commit()
            return redirect(url_for("auth_blueprint.cities", countryID=countryID))
        else:
            form.cityname.data = city.cityName
            form.citycode.data = city.cityCode
            countryID = city.countryID
            return render_template('/admin/editcities.html', form=form, city=city, country=country)
    return render_template('/admin/editcities.html', form=form, cityID=cityID, country=country)

@auth_blueprint.route('/admin/trips/<countryID>/city/<cityID>/remove', methods=['POST', 'GET'])
@login_required
@required_roles('Admin')
def removecity(countryID,cityID):
    city= City.query.filter_by(cityID = cityID).first()
    db.session.delete(city)
    db.session.commit()
    return redirect(url_for("auth_blueprint.cities", countryID=countryID))
# END ADMIN <----------

@auth_blueprint.route('/home')
@login_required
@required_roles('User')
def home():
    user = db.session.query(User).filter(User.id == current_user.id).one()

    received_friend_requests, sent_friend_requests = get_friend_requests(current_user.id)
    num_received_requests = len(received_friend_requests)
    num_sent_requests = len(sent_friend_requests)
    num_total_requests = num_received_requests + num_sent_requests

    # Use a nested dictionary for session["current_user"] to store more than just user_id
    session["current_user"] = {
        "first_name": current_user.first_name,
        "id": current_user.id,
        "num_received_requests": num_received_requests,
        "num_sent_requests": num_sent_requests,
        "num_total_requests": num_total_requests
    }
    return redirect(url_for('auth_blueprint.users', id=user.id))


@auth_blueprint.route('/settings/<username>', methods=['GET', 'POST'])
@login_required
@required_roles('User')
def user_settings(username):
    form = PasswordSettingsForm()
    user = User.query.filter_by(username=username).first()
    if request.method == 'POST':
        if form.validate_on_submit():
            if check_password_hash(current_user.password, request.form['currpassword']):
                current_user.password = generate_password_hash(form.newpassword.data)
                db.session.add(current_user)
                db.session.commit()
                flash('Changes saved!')
                result = User.query.all()
                return render_template('users/settings.html', form=form, result=result)
            else:
                flash('Incorrect Password!')
                return render_template('users/settings.html', form=form, user=user)
        else:
            form.newpassword.data = current_user.password
            return render_template('users/settings.html', form=form, user=user)

    edit = get_edit_friends(user.id).all()

    return render_template('users/settings.html', form=form, user=user, csID=str(current_user.id),
                           csPic=str(get_profile(current_user.profile_pic)), edit=edit)


@auth_blueprint.route("/users/<int:id>")
@login_required
@required_roles('User')
def users(id):
    """Show user profile."""

    # Get current user's friend requests and number of requests to display in badges
    received_friend_requests, sent_friend_requests = get_friend_requests(current_user.id)
    edit_requests = get_edit_requests(current_user.id)
    num_edit_requests = len(edit_requests)
    num_received_requests = len(received_friend_requests)
    num_sent_requests = len(sent_friend_requests)
    num_total_requests = num_received_requests + num_sent_requests + num_edit_requests

    # Use a nested dictionary for session["current_user"] to store more than just user_id
    session["current_user"] = {
        "first_name": current_user.first_name,
        "id": current_user.id,
        "num_received_requests": num_received_requests, "num_sent_requests": num_sent_requests,
        "num_total_requests": num_total_requests, "num_edit_requests": num_edit_requests
    }

    user = db.session.query(User).filter(User.id == id).one()
    trips = Trips.query.filter_by(userID=user.id).all()

    total_friends = len(get_friends(user.id).all())

    user_a_id = session["current_user"]["id"]
    user_b_id = user.id

    # Check connection status between user_a and user_b
    check_friends, pending_request = is_friends_or_pending(user_a_id, user_b_id)
    check_friends2, pending_request2 = is_friends_or_pending2(user_a_id, user_b_id)
    check_request, pending = is_permitted_or_pending(user_a_id, user_b_id)
    check_request2, pending2 = is_permitted_or_pending2(user_a_id, user_b_id)

    friends = get_friends(user.id).all()
    photos = Photos.query.filter_by(userID=user.id).all()

    return render_template("users/user.html",
                           user=user,
                           total_friends=total_friends,
                           check_friends=check_friends,
                           friends=friends, check_request=check_request,
                           check_request2=check_request2, pending=pending,
                           pending_request=pending_request,
                           pending_request2=pending_request2,
                           csID=str(user.id), csPic=str(get_profile(user.profile_pic)),
                           trips=trips, photos=photos)


@auth_blueprint.route('/send-request/<int:id>', methods=["POST"])
@login_required
@required_roles('User')
def edit_request(id):
    """Send a friend request to another user."""

    user = db.session.query(User).filter(User.id == id).one()

    user_x_id = session["current_user"]["id"]
    user_y_id = user.id

    # Check connection status between user_a and user_b
    is_permitted, is_pending = is_permitted_or_pending(user_x_id, user_y_id)

    if user_x_id == user_y_id:
        flash("You send request to yourself.")
        return redirect(url_for('auth_blueprint.users', id=user.id))
    elif is_permitted:
        flash("You are permitted to edit this trip.")
        return redirect(url_for('auth_blueprint.users', id=user.id))
    elif is_pending:
        flash("Your edit request is pending.")
        return redirect(url_for('auth_blueprint.users', id=user.id))
    else:
        requested = Request(user_x_id=user_x_id,
                            user_y_id=user_y_id,
                            status="Requested")
        db.session.add(requested)
        db.session.commit()
        print "User ID %s has sent an edit request to User ID %s" % (user_x_id, user_y_id)
        flash("Request Sent")
        return redirect(url_for('auth_blueprint.users', id=user.id))


@auth_blueprint.route('/add-friend/<int:id>', methods=["POST"])
@login_required
@required_roles('User')
def add_friend(id):
    """Send a friend request to another user."""

    user = db.session.query(User).filter(User.id == id).one()

    user_a_id = session["current_user"]["id"]
    user_b_id = user.id

    # Check connection status between user_a and user_b
    is_friends, is_pending = is_friends_or_pending(user_a_id, user_b_id)

    if user_a_id == user_b_id:
        flash("You cannot add yourself as a friend.")
        return redirect(url_for('auth_blueprint.users', id=user.id))
    elif is_friends:
        flash("You are already friends.")
        return redirect(url_for('auth_blueprint.users', id=user.id))
    elif is_pending:
        flash("Your friend request is pending.")
        return redirect(url_for('auth_blueprint.users', id=user.id))
    else:
        requested_connection = Connection(user_a_id=user_a_id,
                                          user_b_id=user_b_id,
                                          status="Requested")
        db.session.add(requested_connection)
        db.session.commit()
        print "User ID %s has sent a friend request to User ID %s" % (user_a_id, user_b_id)
        flash("Request Sent")
        return redirect(url_for('auth_blueprint.users', id=user.id))


@auth_blueprint.route('/accept-friend/<int:id>', methods=["POST"])
@login_required
@required_roles('User')
def accept_friend(id):
    """Accept a friend request from another user."""

    user = db.session.query(User).filter(User.id == id).one()

    user_a_id = session["current_user"]["id"]
    user_b_id = user.id

    if user_a_id == user_b_id:
        flash("You cannot add yourself as a friend.")
        return redirect(url_for('auth_blueprint.users', id=user.id))
    else:
        requested_connection = Connection(user_a_id=user_a_id,
                                          user_b_id=user_b_id,
                                          status="Accepted")

        requested_connection2 = Connection(user_a_id=user_b_id,
                                           user_b_id=user_a_id,
                                           status="Accepted")

        Connection.query.filter_by(user_a_id=user_b_id,
                                   user_b_id=user_a_id,
                                   status="Requested").delete()

        db.session.add(requested_connection)
        db.session.add(requested_connection2)
        db.session.commit()
        print "User ID %s and User ID %s are now friends." % (user_a_id, user_b_id)
        flash("Request Accepted")
        return redirect(url_for('auth_blueprint.users', id=user.id))


@auth_blueprint.route('/reject-friend/<int:id>', methods=["POST"])
@login_required
@required_roles('User')
def reject_friend(id):
    """Reject a friend request from another user."""

    user = db.session.query(User).filter(User.id == id).one()

    user_a_id = session["current_user"]["id"]
    user_b_id = user.id

    if user_a_id == user_b_id:
        flash("Error.")
        return redirect(url_for('auth_blueprint.users', id=user.id))
    else:
        Connection.query.filter_by(user_a_id=user_b_id,
                                   user_b_id=user_a_id,
                                   status="Requested").delete()
        db.session.commit()
        print "User ID %s and User ID %s are not friends." % (user_a_id, user_b_id)
        return redirect(url_for('auth_blueprint.users', id=user.id))


@auth_blueprint.route('/unfriend/<int:id>', methods=["POST"])
@login_required
@required_roles('User')
def unfriend(id):
    """Unfriend another user."""

    user = db.session.query(User).filter(User.id == id).one()

    user_a_id = session["current_user"]["id"]
    user_b_id = user.id

    if user_a_id == user_b_id:
        flash("Cannot unfriend yourself.")
        return redirect(url_for('auth_blueprint.users', id=user.id))
    else:
        Connection.query.filter_by(user_a_id=user_a_id,
                                   user_b_id=user_b_id,
                                   status="Accepted").delete()

        Connection.query.filter_by(user_a_id=user_b_id,
                                   user_b_id=user_a_id,
                                   status="Accepted").delete()

        db.session.commit()
        print "User ID %s and User ID %s are not friends." % (user_a_id, user_b_id)
        return redirect(url_for('auth_blueprint.users', id=user.id))


@auth_blueprint.route('/disallow/<int:id>', methods=["POST"])
@login_required
@required_roles('User')
def disallow(id):

    user = db.session.query(User).filter(User.id == id).one()

    user_x_id = session["current_user"]["id"]
    user_y_id = user.id

    if user_x_id == user_y_id:
        flash("Cannot disallow yourself.")
        return redirect(url_for('auth_blueprint.user_settings', username=current_user.username))
    else:
        Request.query.filter_by(user_x_id=user_x_id,
                                   user_y_id=user_y_id,
                                   status="Accepted").delete()

        Request.query.filter_by(user_x_id=user_y_id,
                                user_y_id=user_x_id,
                                status="Accepted").delete()

        db.session.commit()
        print "User ID %s disallowed User ID %s to edit trips/itineraries." % (user_x_id, user_y_id)
        return redirect(url_for('auth_blueprint.user_settings', username=current_user.username))


@auth_blueprint.route('/paginateUserFriends')
def paginateUserFriends():
    firstname, lastname, address, city, cas, usID = ([] for i in range(6))
    page_string = request.args.get('page')

    # again assigning query objects to different list to enable jsonify function to return the results
    users = User.query.filter(User.id!=current_user.id).paginate(int(page_string), POSTS_PER_PAGE, False)
    for user in users.items:
        firstname.append(user.first_name)
        lastname.append(user.last_name)
        address.append(user.address)
        city.append(user.city)
        cas.append(str(get_profile(user.profile_pic)))
        usID.append(str(user.id))

    return jsonify(fname=firstname,
                   lname=lastname,
                   addr=address,
                   ct=city,
                   cas=cas,
                   id=usID,
                   size=len(usID))

@auth_blueprint.route('/notifications')
@login_required
@required_roles('User')
def notifications():
    cas = []
    usID = []
    users = User.query.filter(User.id!=current_user.id).paginate(1, POSTS_PER_PAGE, False)
    resAllCount = User.query.filter(User.id!=current_user.id).count()

    numm=resAllCount/POSTS_PER_PAGE
    if resAllCount%POSTS_PER_PAGE!=0:
        numm=(resAllCount/POSTS_PER_PAGE)+1;

    for user in users.items:
        cas.append(str(get_profile(user.profile_pic)))
        usID.append(str(user.id))

    # This returns User objects for current user's friend requests
    received_friend_requests, sent_friend_requests = get_friend_requests(session["current_user"]["id"])
    received_edit_requests = get_edit_requests(session["current_user"]["id"])

    # This returns a query for current user's friends (not User objects), but adding .all() to the end gets list of User objects
    friends = get_friends(session["current_user"]["id"]).all()

    return render_template("users/notification.html",
                           received_friend_requests=received_friend_requests,
                           sent_friend_requests=sent_friend_requests,
                           received_edit_requests=received_edit_requests,
                           friends=friends,
                           users=users,
                           numm=numm, csPic=cas, usID=usID)


@auth_blueprint.route('/accept-request/<int:id>', methods=["POST"])
@login_required
@required_roles('User')
def accept_request(id):
    """Accept a edit request from another user."""

    user = db.session.query(User).filter(User.id == id).one()

    user_x_id = session["current_user"]["id"]
    user_y_id = user.id

    if user_x_id == user_y_id:
        flash("You cannot send request to yourself.")
        return redirect(url_for('auth_blueprint.notifications'))
    else:
        requested = Request(user_x_id=user_x_id,
                            user_y_id=user_y_id,
                            status="Accepted")

        requested2 = Request(user_x_id=user_y_id,
                             user_y_id=user_x_id,
                             status="Accepted")

        Request.query.filter_by(user_x_id=user_y_id,
                                user_y_id=user_x_id,
                                status="Requested").delete()

        db.session.add(requested)
        db.session.add(requested2)
        db.session.commit()
        print "User ID %s can now edit User ID %s's trips/itineraries." % (user_x_id, user_y_id)
        flash("Request Accepted")
        return redirect(url_for('auth_blueprint.notifications'))


@auth_blueprint.route('/reject-request/<int:id>', methods=["POST"])
@login_required
@required_roles('User')
def reject_request(id):
    """Reject a edit request from another user."""

    user = db.session.query(User).filter(User.id == id).one()

    user_x_id = session["current_user"]["id"]
    user_y_id = user.id

    if user_x_id == user_y_id:
        flash("Error.")
        return redirect(url_for('auth_blueprint.notifications'))
    else:
        Request.query.filter_by(user_x_id=user_y_id,
                                user_y_id=user_x_id,
                                status="Requested").delete()
        db.session.commit()
        print "User ID %s cannot edit User ID %s's trips/itineraries." % (user_x_id, user_y_id)
        return redirect(url_for('auth_blueprint.notifications'))

@auth_blueprint.route('/friends')
@auth_blueprint.route('/friends/')
@login_required
@required_roles('User')
def show_friends():
    """Show friend requests and list of all friends"""
    cas = []
    usID = []
    users = User.query.filter(User.id!=current_user.id).paginate(1, POSTS_PER_PAGE, False)
    resAllCount = User.query.filter(User.id!=current_user.id).count()

    numm=resAllCount/POSTS_PER_PAGE
    if resAllCount%POSTS_PER_PAGE!=0:
        numm=(resAllCount/POSTS_PER_PAGE)+1;

    for user in users.items:
        cas.append(str(get_profile(user.profile_pic)))
        usID.append(str(user.id))

    # users = User.query.order_by(desc(User.id)).paginate(page, POSTS_PER_PAGE, False)
    # This returns User objects for current user's friend requests
    received_friend_requests, sent_friend_requests = get_friend_requests(session["current_user"]["id"])

    # This returns a query for current user's friends (not User objects), but adding .all() to the end gets list of User objects
    friends = get_friends(session["current_user"]["id"]).all()

    return render_template("users/friends.html",
                           received_friend_requests=received_friend_requests,
                           sent_friend_requests=sent_friend_requests,
                           friends=friends,
                           users=users,
                           numm=numm, csPic=cas, usID=usID)

@auth_blueprint.route("/friends/search/", methods=["GET", "POST"])
@login_required
@required_roles('User')
def search_users():
    """Search for a user and return results."""

    page = 1
    cas = []
    usID = []
    userr = User.query.order_by(desc(User.id)).paginate(page, POSTS_PER_PAGE, False)
    resAllCount = User.query.filter(User.id != current_user.id).count()

    numm = resAllCount / POSTS_PER_PAGE
    if resAllCount % POSTS_PER_PAGE != 0:
        numm = (resAllCount / POSTS_PER_PAGE) + 1;

    for user in userr.items:
        cas.append(str(get_profile(user.profile_pic)))
        usID.append(str(user.id))

    # Returns users for current user's friend requests
    received_friend_requests, sent_friend_requests = get_friend_requests(session["current_user"]["id"])

    # Returns query for current user's friends (not User objects) so add .all() to the end to get list of User objects
    friends = get_friends(session["current_user"]["id"]).all()
    return render_template("users/browse_friends.html",
                           received_friend_requests=received_friend_requests,
                           sent_friend_requests=sent_friend_requests,
                           friends=friends, userr=userr, page=page,
                           numm=numm, users=user_query(request.args.get('q')),
                           csPic=cas, usID=usID)

@auth_blueprint.route('/userprofile/<username>')
@login_required
@required_roles('User')
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('users/userprofile.html', user=user, csID=str(current_user.id),
                           csPic=str(get_profile(current_user.profile_pic)))


@auth_blueprint.route('/userprofile/<username>/edit', methods=['GET', 'POST'])
@login_required
@required_roles('User')
def edit(username):
    user = User.query.filter_by(username=username).first()
    form = EditForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.address = form.address.data
        current_user.city = form.city.data
        current_user.country = form.country.data
        current_user.birth_date = form.birth_date.data
        current_user.contact_num = form.contact_num.data
        current_user.description = form.description.data
        current_user.gender = form.gender.data

        # location for the image that will be saved
        now_loc = img_folder + str(current_user.id)
        # if directory is not yet created this function will create it
        if os.path.isdir(now_loc) == False:
            os.makedirs(now_loc)

        # if the file field is ever empty or still none
        if form.file.data.filename == None or form.file.data.filename == '':
            current_user.profile_pic = current_user.profile_pic
        else:
            # image saving process
            # checks if the image that was chosen is in the allowed extensions
            if form.file.data and allowed_file(form.file.data.filename):
                # securing the filename
                filename = secure_filename(form.file.data.filename)
                # initially saving the image
                form.file.data.save(os.path.join(now_loc + '/', filename))

                uploadFolder = now_loc + '/'

                # the renaming process of the image
                nameNow = str(int(time.time())) + '.' + str(os.path.splitext(filename)[1][1:])

                # saving the changes
                os.rename(uploadFolder + filename, uploadFolder + nameNow)

                # this is the compressor part, this will optimize the image
                # and will decrease its file size but not losing that much quality
                img = Image.open(open(str(uploadFolder + nameNow), 'rb'))
                img.save(str(uploadFolder + nameNow), quality=90, optimize=True)

            # this is where the new filename will be saved to the db
            date = datetime.datetime.today().strftime('%m/%d/%y')
            photo = Photos(photoName=nameNow, photoDate=date, photoLocation=now_loc, userID=current_user.id)
            db.session.add(photo)
            db.session.commit()

            ph_1 = Photos.query.filter_by(userID=current_user.id).all()
            for p in ph_1:
                if p.photoName == str(nameNow):
                    current_user.profile_pic = p.id

        db.session.add(current_user)
        db.session.commit()

        flash("Your changes have been saved.")
        return render_template('users/userprofile.html', user=user, csID=str(current_user.id),
                               csPic=str(get_profile(current_user.profile_pic)))
    else:
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.address.data = current_user.address
        form.city.data = current_user.city
        form.country.data = current_user.country
        form.birth_date.data = current_user.birth_date
        form.contact_num.data = current_user.contact_num
        form.description.data = current_user.description
        form.gender.data = current_user.gender

        return render_template('users/edit_profile.html', user=user, form=form, csID=str(current_user.id),
                               csPic=str(get_profile(current_user.profile_pic)))


@auth_blueprint.route('/user/photos')
@login_required
@required_roles('User')
def select_photo():
    user = db.session.query(User).filter(User.id == current_user.id).one()
    photos = Photos.query.filter_by(userID=current_user.id).all()

    return render_template('users/photos.html', username=current_user.username, csID=str(current_user.id),
                           csPic=str(get_profile(current_user.profile_pic)), user=user, photos=photos)


@auth_blueprint.route('/set_profile')
@login_required
@required_roles('User')
def modify_prophoto():
    current_user.profile_pic = int(request.args.get('id'))
    db.session.add(current_user)
    db.session.commit()

    return jsonify(response='ok', userid=current_user.id, filename=get_profile(current_user.profile_pic))


# for reset password
@auth_blueprint.route('/reset_request', methods=['GET', 'POST'])
def reset():
    token = request.args.get('token', None)
    form = EmailResetForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            # gets token
            token = user.get_token()
            body = 'Click this link to reset your password:' + '\n' + '127.0.0.1:5000/reset/' + token
            # sends an email containg the route with token value to the user who wants to reset his/her password
            send_email('Password Reset', app.config['MAIL_USERNAME'], [str(email)], body)
            flash("Request Sent!")
            return render_template('users/mail_send.html')
    flash('Something went wrong!')
    return render_template('users/reset.html', form=form)


@auth_blueprint.route('/reset/<token>', methods=['GET', 'POST'])
def reset_now(token):
    # verifies the token if its still not expired yet and then gets the user associated with the token
    user_exist = User.verify_token(token)
    form = PasswordResetForm()
    if token and user_exist:
        is_verified_token = True
        if form.validate_on_submit():
            # reseting password process
            user_exist.password = generate_password_hash(form.password.data)
            user_exist.is_active = True
            db.session.add(user_exist)
            db.session.commit()
            flash("password updated successfully")
            return render_template('users/password_changed.html')
    return render_template('users/reset_enable.html', form=form, token=token)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if current_user.is_active():
        return redirect(url_for('landing_blueprint.index'))
    else:
        if request.method == 'POST':
            if form.validate_on_submit():
                user = User.query.filter_by(username=request.form['username']).first()
                if user:
                    if user.role_id == 3:
                        if user is not None and check_password_hash(user.password, request.form['password']):
                            login_user(user)
                            flash('You are now logged in!')

                            # Get current user's friend requests and number of requests to display in badges
                            received_friend_requests, sent_friend_requests = get_friend_requests(current_user.id)
                            edit_requests = get_edit_requests(current_user.id)
                            num_edit_requests = len(edit_requests)
                            num_received_requests = len(received_friend_requests)
                            num_sent_requests = len(sent_friend_requests)
                            num_total_requests = num_received_requests + num_sent_requests + num_edit_requests

                            # Use a nested dictionary for session["current_user"] to store more than just user_id
                            session["current_user"] = {
                                "first_name": current_user.first_name,
                                "id": current_user.id,
                                "num_received_requests": num_received_requests,
                                "num_sent_requests": num_sent_requests,
                                "num_total_requests": num_total_requests,
                                "num_edit_requests": num_edit_requests
                            }
                        if user.first_login == True:
                            user.first_login = False
                            db.session.add(user)
                            db.session.commit()
                            flash('You are now logged in!')
                            return redirect(url_for('auth_blueprint.edit', username=request.form['username']))
                        flash('You are now logged in!')
                        return redirect(url_for('auth_blueprint.home', name=request.form['username']))
                    elif user.role_id == 1:
                        if user is not None and check_password_hash(user.password, request.form['password']):
                            login_user(user)
                            flash('You are now logged in!')
                        return redirect(url_for('auth_blueprint.addash', name=request.form['username']))
                    else:
                        flash('ERROR! Incorrect login credentials-1', 'error')
                        return redirect(url_for('landing_blueprint.index'))
                else:
                    flash('user not found!')
                    return render_template('users/signin.html', form=form)
            else:
                error = 'Invalid username or password'
                flash('ERROR! Incorrect login credentials-2', 'error')
                return render_template('users/signin.html', form=form, error=error)
        else:
            error = 'Invalid username or password'
        flash('Please log in!', 'error')
        return render_template('users/signin.html', form=form, error=error)


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    Role.insert_roles()
    if current_user.is_active():
        flash('Continue')
        return redirect(url_for('landing_blueprint.index'))
    else:
        if form.validate_on_submit():
            user = User(username=request.form['username'], email=request.form['email'],
                        password=request.form['password'], role_id=3)
            db.session.add(user)
            db.session.commit()

            # Add same info to session for new user as per /login route
            session["current_user"] = {
                "first_name": user.first_name,
                "id": user.id,
                "num_received_requests": 0,
                "num_sent_requests": 0,
                "num_total_requests": 0,
                "num_edit_requests": 0
            }

            flash('Please log in')
            return redirect(url_for('auth_blueprint.login'))
        flash('Register!')
        return render_template('users/registration.html', form=form)


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('auth_blueprint.login'))

@auth_blueprint.route('/')
def initial():
    return render_template('users/initial.html')
