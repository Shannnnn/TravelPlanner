import os
from functools import wraps
from flask import abort, flash
from flask_login import current_user
from model import Role, Connection, User, db, Photos, Request
from app.trips.model import Trips
from sqlalchemy import func

# this will determine if the user is authenticated to go to a certain route
def required_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_role() not in roles:
                abort(403)
                flash('Authentication error, please check your details and try again', 'error')
            return f(*args, **kwargs)

        return wrapped

    return wrapper


def get_role():
    role = Role.query.filter_by(id=current_user.role_id).first()
    return role.name


def is_friends_or_pending(user_a_id, user_b_id):
    """
    Checks the friend status between user_a and user_b.
    Checks if user_a and user_b are friends.
    Checks if there is a pending friend request from user_a to user_b.
    """

    is_friends = db.session.query(Connection).filter(Connection.user_a_id == user_a_id,
                                                     Connection.user_b_id == user_b_id,
                                                     Connection.status == "Accepted").first()

    is_pending = db.session.query(Connection).filter(Connection.user_a_id == user_a_id,
                                                     Connection.user_b_id == user_b_id,
                                                     Connection.status == "Requested").first()

    return is_friends, is_pending


def is_friends_or_pending2(user_a_id, user_b_id):
    """
    Checks the friend status between user_a and user_b.
    Checks if user_a and user_b are friends.
    Checks if there is a pending friend request from user_b to user_a.
    """

    is_friends = db.session.query(Connection).filter(Connection.user_a_id == user_b_id,
                                                     Connection.user_b_id == user_a_id,
                                                     Connection.status == "Accepted").first()

    is_pending = db.session.query(Connection).filter(Connection.user_a_id == user_b_id,
                                                     Connection.user_b_id == user_a_id,
                                                     Connection.status == "Requested").first()

    return is_friends, is_pending


def get_friend_requests(id):
    """
    Get user's friend requests.
    Returns users that user received friend requests from.
    Returns users that user sent friend requests to.
    """

    received_friend_requests = db.session.query(User).filter(Connection.user_b_id == id,
                                                             Connection.status == "Requested").join(Connection,
                                                                                                    Connection.user_a_id == User.id).all()

    sent_friend_requests = db.session.query(User).filter(Connection.user_a_id == id,
                                                         Connection.status == "Requested").join(Connection,
                                                                                                Connection.user_b_id == User.id).all()

    return received_friend_requests, sent_friend_requests


def get_friends(id):
    """
    Return a query for user's friends
    Note: This does not return User objects, just the query
    """

    friends = db.session.query(User).filter(Connection.user_a_id == id,
                                            Connection.status == "Accepted").join(Connection,
                                                                                  Connection.user_b_id == User.id)

    return friends


def is_permitted_or_pending(user_x_id, user_y_id):

    is_permitted = db.session.query(Request).filter(Request.user_x_id == user_x_id,
                                                       Request.user_y_id == user_y_id,
                                                       Request.status == "Accepted").first()

    is_pending = db.session.query(Request).filter(Request.user_x_id == user_x_id,
                                                     Request.user_y_id == user_y_id,
                                                     Request.status == "Requested").first()

    return is_permitted, is_pending

def is_permitted_or_pending2(user_x_id, user_y_id):

    is_permitted = db.session.query(Request).filter(Request.user_x_id == user_y_id,
                                                       Request.user_y_id == user_x_id,
                                                       Request.status == "Accepted").first()

    is_pending = db.session.query(Request).filter(Request.user_x_id == user_y_id,
                                                     Request.user_y_id == user_x_id,
                                                     Request.status == "Requested").first()

    return is_permitted, is_pending


def get_edit_requests(id):

    edit_requests = db.session.query(User).filter(Request.user_y_id == id,
                                                 Request.status == "Requested").join(Request,
                                                                                     Request.user_x_id == User.id).all()


    return edit_requests


def get_edit_friends(id):

    edit = db.session.query(User).filter(Request.user_x_id == id,
                                         Request.status == "Accepted").join(Request,
                                                                            Request.user_y_id == User.id)

    return edit

# the current directory for user profile pic
img_folder = 'app/auth/static/images/users/'
#img_folder = 'app/uploads/static/images/users/'


# determines the only allowed file extensions for images
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in set(['png', 'jpg', 'PNG', 'JPG'])

def deleteTrip_user(userID):
    trips = Trips.query.filter_by(userID=userID).all()
    for trip in trips:
        os.remove('app/trips/static/images/trips/'+str(userID) +'/' + trip.img_thumbnail)
        db.session.delete(trip)
    db.session.commit()


def user_query(var):
    return db.session.query(User).filter(
        func.concat(User.username, ' ', User.first_name, ' ', User.last_name).like('%' + var + '%')).all()


def determine_pic(users, counter):
    user_photos = []
    if counter == 0:
        user_photos.append(return_res_for_pic(users))
    else:
        for r in users:
            user_photos.append(return_res_for_pic(r))
    return user_photos


def return_res_for_pic(user):
    photo = ""
    ph = Photos.query.filter_by(id=user.profile_pic).first()
    if ph is None:
        photo = "default"
    else:
        photo = str(ph.photoName)
    return photo