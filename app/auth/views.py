import os
from flask import Flask, render_template, redirect, Blueprint, request, flash, url_for, session, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, AnonymousUserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from model import User, Role, Anonymous, Photos, Connection
from forms import LoginForm, RegisterForm, EditForm, SearchForm, PasswordSettingsForm, UsernameSettingsForm
from app import db, app
from decorators import required_roles, get_friends, get_friend_requests, allowed_file, deleteTrip_user, img_folder, is_friends_or_pending, user_query_1
from app.landing.views import landing_blueprint
from werkzeug import secure_filename
from PIL import Image
from app.trips.model import Trips, Itineraries
from app.trips.forms import EditTripForm, ItineraryForm, EditItineraryForm
from app.landing.views import determine_pic
import datetime
import time
from sqlalchemy import desc

auth = Flask(__name__)
auth_blueprint = Blueprint('auth_blueprint', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_blueprint.login'
login_manager.anonymous_user = Anonymous

POSTS_PER_PAGE = 9
page = 1

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
    return render_template('admin/admindashboard.html', users=users, trips=trips)

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
                return render_template('admin/users.html', form=form, result=result)
            else:
                flash('Incorrect Password!')
                return render_template('admin/settings.html', form=form, user=user)
        else:
            form.newpassword.data = current_user.password
            return render_template('admin/settings.html', form=form, user=user)
    return render_template('admin/settings.html', form=form, user=user)

@auth_blueprint.route('/admin/settings/username/<username>', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def usernamesettings(username):
    form = UsernameSettingsForm()
    form1 = PasswordSettingsForm()
    user = User.query.filter_by(username=username).first()
    if request.method == 'POST':
        if form.validate_on_submit():
            if check_password_hash(current_user.password, request.form['currpassword']):
                current_user.username = form.username.data
                db.session.add(current_user)
                db.session.commit()
                flash('Changes saved!')
                result = User.query.all()
                return render_template('admin/users.html', form=form, result=result)
            else:
                flash('Invalid Username!')
                return render_template('admin/usernamesettings.html', form=form, user=user, form1=form1)
        else:
            form.username.data = current_user.username
            return render_template('admin/usernamesettings.html', form=form, user=user, form1=form1)
    return render_template('admin/usernamesettings.html', form=form, user=user, form1=form1)

@auth_blueprint.route('/admin/users/sort/admin', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def sortadmin():
    result = User.query.filter_by(role_id='1')
    return render_template('admin/users.html', result=result)

@auth_blueprint.route('/admin/users/sort/moderator', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def sortmod():
    result = User.query.filter_by(role_id='2')
    return render_template('admin/users.html', result=result)

@auth_blueprint.route('/admin/users/sort/member', methods=['GET', 'POST'])
@login_required
@required_roles('Admin')
def sortuser():
    result = User.query.filter_by(role_id='3')
    return render_template('admin/users.html', result=result)

# USERS --> read
@auth_blueprint.route('/admin/users', methods=['GET','POST'])
@login_required
@required_roles('Admin')
def manageusers():
    result = User.query.order_by(User.id)
    return render_template('admin/users.html', result=result)

@auth_blueprint.route('/admin/users/create', methods=['GET','POST'])
@login_required
@required_roles('Admin')
def addusers():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(username=form.username.data,
                               email=form.email.data,
                               password=form.password.data,
                               role_id = "3")
            db.session.add(user)
            db.session.commit()
            result = User.query.order_by(User.id)
            flash("Your changes have been saved.")
            return render_template('admin/users.html', result=result)
    return render_template('admin/createusers.html', form=form)

#update
@auth_blueprint.route('/admin/users/edit/<username>', methods = ['GET', 'POST'])
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
        result = User.query.all()
        return render_template('admin/users.html', result=result, user=user, csID=str(user.id), csPic=str(cas))
    else:
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.address.data = user.address
        form.city.data = user.city
        form.country.data = user.country
        form.birth_date.data = user.birth_date
        form.contact_num.data = user.contact_num
        form.description.data = user.description

        ph = Photos.query.filter_by(id=user.profile_pic).first()
        if ph is None:
            cas = 'default'
        else:
            cas = ph.photoName
        return render_template('admin/editusers.html', user=user, form=form, csID=str(user.id),
                               csPic=str(cas))

#delete
@auth_blueprint.route('/admin/users/remove/<username>', methods=['GET','POST'])
@login_required
@required_roles('Admin')
def deleteusers(username):
    user = User.query.filter_by(username=username).first()
    deleteTrip_user(user.id)
    if user.profile_pic!='default':
        os.remove(img_folder+str(user.profile_pic))
    db.session.delete(user)
    db.session.commit()
    result = User.query.all()
    return render_template('admin/users.html', result = result)

# TRIPS --> read
@auth_blueprint.route('/admin/trips')
@login_required
@required_roles('Admin')
def managetrips():
    result = Trips.query.all()
    return render_template('admin/trips.html', result=result)

#delete
@auth_blueprint.route('/admin/trips/remove/<tripName>', methods=['GET','POST'])
@login_required
@required_roles('Admin')
def removetrips(tripName):
    trips = Trips.query.filter_by(tripName=tripName).first()
    os.remove('app/trips/static/images/trips/'+trips.img_thumbnail)
    db.session.delete(trips)
    db.session.commit()
    result = Trips.query.all()
    return render_template('admin/trips.html', result=result)

# update
@auth_blueprint.route('/admin/trips/edit/<tripName>', methods=['GET','POST'])
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
            return redirect(url_for("auth_blueprint.managetrips"))
        return render_template('/admin/trip.html', trips=trips)
    else:
        form.trip_name.data = tripname.tripName
        form.trip_date_from.data = tripname.tripDateFrom
        form.trip_date_to.data = tripname.tripDateTo
    return render_template('/admin/edittrips.html', form=form, tripname=tripname)

@auth_blueprint.route('/admin/trips/<tripName>/itineraries', methods=['GET'])
def itineraries(tripName):
    tripid = Trips.query.filter_by(tripName=tripName).first()
    itinerary = Itineraries.query.filter_by(tripID=tripid.tripID)
    trip = Trips.query.filter_by(userID=current_user.id, tripName=tripName).first()
    return render_template('/admin/itineraries.html', trip=trip, itineraries=itinerary)

@auth_blueprint.route('/admin/trips/<tripName>/<itineraryName>/edit', methods=['GET', 'POST'])
def editItineraries(tripName, itineraryName):
    tripname = Trips.query.filter_by(tripName=tripName).first()
    itineraryname = Itineraries.query.filter_by(tripID=tripname.tripID, itineraryName=itineraryName).first()
    itineraries = Itineraries.query.all()
    form = EditItineraryForm()
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
            return redirect(url_for("auth_blueprint.itineraries", tripName=tripName))
        return render_template('/admin/itineraries.html', trip=tripname, itineraries=itineraries)
    else:
        form.itinerary_name.data = itineraryname.itineraryName
        form.itinerary_date_from.data = itineraryname.itineraryDateFrom
        form.itinerary_date_to.data = itineraryname.itineraryDateTo
        form.itinerary_desc.data = itineraryname.itineraryDesc
        form.itinerary_location_type.data = itineraryname.locationTypeID
        form.itinerary_location.data = itineraryname.itineraryLocation
        form.itinerary_time_from.data = itineraryname.itineraryTimeFrom
        form.itinerary_time_to.data = itineraryname.itineraryTimeTo
    return render_template('/admin/edititinerary.html', form=form, tripname=tripname)
# END ADMIN <----------


@auth_blueprint.route('/home')
@login_required
@required_roles('User')
def home():
    user = db.session.query(User).filter(User.id == current_user.id).one()
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
    return render_template('users/settings.html', form=form, user=user)


@auth_blueprint.route("/users/<int:id>")
@login_required
@required_roles('User')
def users(id):
    """Show user profile."""

    # Get current user's friend requests and number of requests to display in badges
    received_friend_requests, sent_friend_requests = get_friend_requests(current_user.id)
    num_received_requests = len(received_friend_requests)
    num_sent_requests = len(sent_friend_requests)
    num_total_requests = num_received_requests + num_sent_requests

    # Use a nested dictionary for session["current_user"] to store more than just user_id
    session["current_user"] = {
        "first_name": current_user.first_name,
        "id": current_user.id,
        "num_received_requests": num_received_requests, "num_sent_requests": num_sent_requests,
        "num_total_requests": num_total_requests
    }

    ph = Photos.query.filter_by(id=current_user.profile_pic).first()
    if ph is None:
        cas = 'default'
    else:
        cas = ph.photoName

    user = db.session.query(User).filter(User.id == id).one()
    trip = Trips.query.filter_by(userID=current_user.id)

    total_friends = len(get_friends(user.id).all())

    user_a_id = session["current_user"]["id"]
    user_b_id = user.id

    # Check connection status between user_a and user_b
    friends, pending_request = is_friends_or_pending(user_a_id, user_b_id)

    friends = get_friends(session["current_user"]["id"]).all()

    return render_template("users/user.html",
                           user=user,
                           total_friends=total_friends,
                           friends=friends,
                           pending_request=pending_request,
                           csID=str(current_user.id), csPic=str(cas),
                           trips=trip)


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
        received_friend_requests = get_friend_requests(current_user.id)
        num_received_requests = len(received_friend_requests) - 1
        requested_connection = Connection(user_a_id=user_a_id,
                                          user_b_id=user_b_id,
                                          status="Accepted")
        db.session.add(requested_connection)
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
        received_friend_requests = get_friend_requests(current_user.id)
        num_received_requests = len(received_friend_requests) - 1
        Connection.query.filter_by(user_a_id=user_a_id,
                                   user_b_id=user_b_id,
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

        db.session.commit()
        print "User ID %s and User ID %s are not friends." % (user_a_id, user_b_id)
        return redirect(url_for('auth_blueprint.users', id=user.id))


@auth_blueprint.route('/friends')
@login_required
@required_roles('User')
def show_friends():
    """Show friend requests and list of all friends"""

    ph = Photos.query.filter_by(id=current_user.profile_pic).first()
    if ph is None:
        cas = 'default'
    else:
        cas = ph.photoName

    users = User.query.order_by(desc(User.id)).paginate(page, POSTS_PER_PAGE, False)

    # This returns User objects for current user's friend requests
    received_friend_requests, sent_friend_requests = get_friend_requests(session["current_user"]["id"])

    # This returns a query for current user's friends (not User objects), but adding .all() to the end gets list of User objects
    friends = get_friends(session["current_user"]["id"]).all()

    return render_template("users/friends.html",
                           received_friend_requests=received_friend_requests,
                           sent_friend_requests=sent_friend_requests,
                           friends=friends, users=users, page=page,
                           csID=str(current_user.id), csPic=str(cas))


@auth_blueprint.route("/friends/search/", methods=["GET", "POST"])
@auth_blueprint.route('/friends/search/<int:page>', methods=['GET', 'POST'])
@login_required
@required_roles('User')
def search_users(page=1):
    """Search for a user and return results."""

    ph = Photos.query.filter_by(id=current_user.profile_pic).first()
    if ph is None:
        cas = 'default'
    else:
        cas = ph.photoName

    userr = User.query.order_by(desc(User.id)).paginate(page, POSTS_PER_PAGE, False)

    # Returns users for current user's friend requests
    received_friend_requests, sent_friend_requests = get_friend_requests(session["current_user"]["id"])

    # Returns query for current user's friends (not User objects) so add .all() to the end to get list of User objects
    friends = get_friends(session["current_user"]["id"]).all()

    return render_template("users/browse_friends.html",
                           received_friend_requests=received_friend_requests,
                           sent_friend_requests=sent_friend_requests,
                           friends=friends, userr=userr, page=page,
                           csID=str(current_user.id), csPic=str(cas),
                           users=user_query_1(request.args.get('q')),
                           photo=determine_pic(user_query_1(request.args.get('q')), 1))


@auth_blueprint.route('/userprofile/<username>')
@login_required
@required_roles('User')
def user_profile(username):
    ph = Photos.query.filter_by(id=current_user.profile_pic).first()
    if ph is None:
        cas = 'default'
    else:
        cas = ph.photoName
    user = User.query.filter_by(username=username).first()
    return render_template('users/userprofile.html', user=user, csID=str(current_user.id), csPic=str(cas))

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

        now_loc = img_folder+str(current_user.id)
        if os.path.isdir(now_loc)==False:
            os.makedirs(now_loc)

        if form.file.data.filename==None or form.file.data.filename=='':
            current_user.profile_pic = current_user.profile_pic
        else:  
            if form.file.data and allowed_file(form.file.data.filename):
                filename = secure_filename(form.file.data.filename)
                form.file.data.save(os.path.join(now_loc+'/', filename))

                uploadFolder = now_loc+'/'
                nameNow = str(int(time.time()))+'.'+str(os.path.splitext(filename)[1][1:])
                os.rename(uploadFolder+filename, uploadFolder+nameNow)

            date = datetime.datetime.today().strftime('%m/%d/%y')
            photo = Photos(photoName=nameNow, photoDate=date, photoLocation=now_loc, userID=current_user.id)          
            db.session.add(photo)
            db.session.commit()

            ph_1 = Photos.query.filter_by(userID=current_user.id).all()
            for p in ph_1:
                if p.photoName==str(nameNow):
                    current_user.profile_pic=p.id

        db.session.add(current_user)
        db.session.commit()

        ph = Photos.query.filter_by(id=current_user.profile_pic).first()
        if ph is None:
            cas = 'default'
        else:
            cas = ph.photoName

        flash("Your changes have been saved.")
        return render_template('users/userprofile.html', user=user, csID=str(current_user.id), csPic=str(cas))
    else:
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.address.data = current_user.address
        form.city.data = current_user.city
        form.country.data = current_user.country
        form.birth_date.data = current_user.birth_date
        form.contact_num.data = current_user.contact_num
        form.description.data = current_user.description

        ph = Photos.query.filter_by(id=current_user.profile_pic).first()
        if ph is None:
            cas = 'default'
        else:
            cas = ph.photoName
        return render_template('users/edit_profile.html', user=user, form=form, csID=str(current_user.id), csPic=str(cas))

@auth_blueprint.route('/user/photos')
@login_required
@required_roles('User')
def select_photo():
    ph = Photos.query.filter_by(id=current_user.profile_pic).first()
    user = db.session.query(User).filter(User.id == current_user.id).one()

    if ph is None:
        cas = 'default'
    else:
        cas = ph.photoName

    photos = Photos.query.filter_by(userID=current_user.id).all()

    return render_template('users/photos.html', username=current_user.username, csID=str(current_user.id), csPic=str(cas), user=user, photos=photos)

@auth_blueprint.route('/set_profile')
@login_required
@required_roles('User')
def modify_prophoto():
    current_user.profile_pic = int(request.args.get('id'))
    db.session.add(current_user)
    db.session.commit()

    ph = Photos.query.filter_by(id=current_user.profile_pic).first()

    if ph is None:
        cas = 'default'
    else:
        cas = ph.photoName 
    return jsonify(response='ok', userid=current_user.id, filename=cas)

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
                if user.role_id == 3:
                    if user is not None and check_password_hash(user.password, request.form['password']):
                        login_user(user)
                        flash('You are now logged in!')
                    if user.first_login == True:
                        user.first_login = False
                        db.session.add(user)
                        db.session.commit()
                        return redirect(url_for('auth_blueprint.edit', username=request.form['username']))

                    # Get current user's friend requests and number of requests to display in badges
                    received_friend_requests, sent_friend_requests = get_friend_requests(current_user.id)
                    num_received_requests = len(received_friend_requests)
                    num_sent_requests = len(sent_friend_requests)
                    num_total_requests = num_received_requests + num_sent_requests

                    # Use a nested dictionary for session["current_user"] to store more than just user_id
                    session["current_user"] = {
                        "first_name": current_user.first_name,
                        "id": current_user.id,
                        "num_received_requests": num_received_requests,                            "num_sent_requests": num_sent_requests,
                        "num_total_requests": num_total_requests
                    }

                    return redirect(url_for('auth_blueprint.home', name=request.form['username']))
                elif user.role_id == 1:
                    if user is not None and check_password_hash(user.password, request.form['password']):
                        login_user(user)
                        flash('You are now logged in!')
                    return redirect(url_for('auth_blueprint.addash', name=request.form['username']))
                else:
                    return redirect(url_for('landing_blueprint.index'))
            else:
                error = 'Invalid username or password'
                return render_template('users/signin.html', form=form, error=error)
        else:
            error = 'Invalid username or password'
        return render_template('users/signin.html', form=form, error=error)

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    Role.insert_roles()
    if current_user.is_active():
        return redirect(url_for('landing_blueprint.index'))
    else:
        if form.validate_on_submit():
            user = User(username=request.form['username'], email=request.form['email'], password=request.form['password'], role_id=3)          
            db.session.add(user)
            db.session.commit()

            # Add same info to session for new user as per /login route
            session["current_user"] = {
                "first_name": user.first_name,
                "id": user.id,
                "num_received_requests": 0,
                "num_sent_requests": 0,
                "num_total_requests": 0
            }

            flash('Log In')
            return redirect(url_for('auth_blueprint.login'))
        return render_template('users/registration.html', form=form)

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('auth_blueprint.login'))
