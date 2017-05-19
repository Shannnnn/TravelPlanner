import os
from functools import wraps
from flask import abort, flash
from flask_login import current_user
from model import Role, Connection, User, db
from app.trips.model import Trips
from sqlalchemy import func

def required_roles(*roles):
   def wrapper(f):
      @wraps(f)
      def wrapped(*args, **kwargs):
         if get_role() not in roles:
            abort(403)
            flash('Authentication error, please check your details and try again','error')
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

def user_query_1(var):
    return db.session.query(User).filter(func.concat(User.username, ' ', User.first_name, ' ', User.last_name).like('%'+var+'%')).all()

img_folder = 'app/auth/static/images/users/'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in set(['png', 'jpg', 'PNG', 'JPG'])

def deleteTrip_user(userID):
    trips = Trips.query.filter_by(userID=userID).all()
    for trip in trips:
        os.remove('app/trips/static/images/trips/'+trip.img_thumbnail)
        db.session.delete(trip)
    db.session.commit()