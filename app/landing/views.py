from flask import Flask, render_template, redirect, Blueprint, request, flash, url_for, jsonify, send_from_directory
from flask_login import current_user
from flask_login import LoginManager, current_user, AnonymousUserMixin
from app import db, app
from decorators import send_email, verify, POSTS_PER_PAGE, maxNum, maxPage, max_for_most, max_for_new, num_of_page
from sqlalchemy import func, desc, or_, and_
from app.trips.model import Trips, Itineraries
from app.auth.model import User, Photos
from model import Anonymous
from sqlalchemy.sql.expression import tuple_

landing = Flask(__name__)
landing_blueprint = Blueprint('landing_blueprint', __name__, template_folder='templates', url_prefix='/main',
                              static_folder='static', static_url_path='/static/')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous

# helper functions
# global variable which is useful in storing values for filter search fucntion
op1 = []


# modification of the global variable through provided parameters
def change_val(var1, var2, var3):
    # first specify that op1 is the global value above
    global op1
    # op1 is being populated
    op1 = [var1, var2, var3]


# returns the value of op1 per server run
def ret_op1():
    return op1


# this is basically all titles what will bbe displayed in the trip-plans template
def tripPlansTitle(n):
    l = ['Most Popular', 'Newest Trips', 'All Trips']
    # returns the proper title to be displayed with given category number
    return l[n]


# this will determine how many pages are to be displayed in the given template
def pageNumberDeterminer(category_count):
    # if the are no excess in the 12 trips per page rule then the following will be returned
    if category_count % (POSTS_PER_PAGE) == 0:
        return category_count / (POSTS_PER_PAGE)
    # if ever there is an excess, then this value below will be returned
    return (category_count / (POSTS_PER_PAGE)) + 1


# this function determines the profile picture of a user
def return_res_for_pic(user):
    ph = Photos.query.filter_by(id=user.profile_pic).first()
    if ph is None:
        # if this will be returned then the photo of the user shall be a gravatar image
        return "default"
    return str(ph.photoName)


# this was supposed to handle 1 or many users profile picture assignment
def determine_pic(users, counter):
    user_photos = []
    # if current user is just one
    if counter == 0:
        user_photos.append(return_res_for_pic(users))
    # if users from parameters specifies many users
    else:
        for r in users:
            # calls the function above every instance of users
            user_photos.append(return_res_for_pic(r))
    return user_photos


# query function helpers
# --> this fucntions were made cause some of them are usable in not just one route but in multiple routes
# --> this functions eliminates rendundancy
# --> some of this queries are missing .all(), .first() cause their use varries in each routes

#basis for some queries
def tripBASE():
    return Trips.query.filter(and_(Trips.status==1, Trips.visibility==0))

# this function will return a query result from the given var
def alternateSearchResult(var):
    return Trips.query.filter(and_(func.concat(Trips.tripName, ' ', Trips.tripDateFrom, ' ', 
        Trips.tripDateTo).ilike('%'+var+'%'), and_(Trips.status==1, Trips.visibility==0)))

# this function is used by the filter search integrated to some templates
def deepSearchResult(var, var2):
    return Trips.query.filter(and_(or_((func.concat(Trips.tripName, ' ', Trips.tripDateFrom, ' ', 
        Trips.tripDateTo).ilike('%'+var+'%')),Trips.tripID.in_(var2)), and_(Trips.status==1, Trips.visibility==0))).distinct()

def mainSearch(num, var):
    tripIDS = []
    itere = Itineraries.query.filter(
        func.concat(Itineraries.itineraryName, ' ', Itineraries.itineraryDesc).ilike('%'+var+'%')).all()
    # if itere has nothing this will be done
    if itere is None:
        # remember the queries above, this where they are useful
        return alternateSearchResult(var).paginate(num, POSTS_PER_PAGE, False), pageNumberDeterminer(len(alternateSearchResult(var).all()))

    # if itere has been populated, then
    for i in itere:
        tripIDS.append(i.tripID)

    return deepSearchResult(var, tripIDS).paginate(num, POSTS_PER_PAGE, False), pageNumberDeterminer(len(deepSearchResult(var, tripIDS).all()))


def categoryResult(n, page_):
    if n == 0:
        # this will be returned if ever the category that has been selected is Most Viewed Trips
        return tripBASE().order_by(desc(Trips.viewsNum)).paginate(page_, POSTS_PER_PAGE, False)
    elif n == 1:
        # this will be returned if ever the category that has been selected is Newest Trips
        return tripBASE().order_by(desc(Trips.tripID)).paginate(page_, POSTS_PER_PAGE, False)
    # if n above is not satisfied, then the category that has been selected was All Trips
    return Trips.query.filter(and_(Trips.status==1, Trips.visibility==0)).paginate(page_, POSTS_PER_PAGE, False)


# this will handle the dynamic pagination of filter search result
def filterSearchResultHandler(n, base_string1, base_string2):
    if n == 0:
        # this is for the Most Vieded Trips
        # what this does, is that it check if base_string1 or base_string2 has likely match in the Trips table and then
        # ----it shall also satisfy the condition that the return result from above is in the premises of Most Viewed Category
        return Trips.query.filter(and_(and_((Trips.tripCountry).ilike('%'+base_string1+'%')), (Trips.tripCity).ilike('%'+base_string2+'%')),
                    and_(Trips.status==1, Trips.visibility==0)).order_by(Trips.viewsNum)

    # this is for All trips and Newest Trips
    return Trips.query.filter(and_(and_((Trips.tripCountry).ilike('%'+base_string1+'%')), (Trips.tripCity).ilike('%'+base_string2+'%')),
                    and_(Trips.status==1, Trips.visibility==0)).order_by(desc(Trips.tripID))

    
    




# routes
@landing_blueprint.route('/')
@landing_blueprint.route('/index')
def index():
    featured = Trips.query.filter(and_(Trips.status==1, Trips.visibility==0)).order_by(func.random()).limit(4)
    #Newest trips
    trip_index = tripBASE().order_by(desc(Trips.tripID)).paginate(1, 4, False)
    #Most Viewed Trips
    trip_index_most = tripBASE().order_by(desc(Trips.viewsNum)).paginate(1, 4, False)
    return render_template('index.html', 
                            title='TravelPlanner-Home', 
                            featured=featured, 
                            trips=trip_index, 
                            trips_m=trip_index_most,
                            label=verify(), 
                            collide=True)


@landing_blueprint.route('/about')
@landing_blueprint.route('/about/')
def about():
    return render_template('about.html', title='About', label=verify(), collide=True)


@landing_blueprint.route('/response')
@landing_blueprint.route('/response/')
def sendUs():
    return render_template('response.html', title='Response', label=verify(), collide=True)


# this is the route for the searchbar on top of the page
@landing_blueprint.route('/siteSearch', methods=['GET', 'POST'])
def siteSearch():
    trips, main_count = mainSearch(1, request.args.get('search_1'))
    return render_template('search.html', 
                            title='Search Result', 
                            label=verify(),
                            trips=trips, 
                            stry=request.args.get('search_1'), 
                            numm=main_count, 
                            collide=False, 
                            path=0)


# the dynamic pagination for /siteSearch result
@landing_blueprint.route('/search_main_/<keyword>')
def paginate_search(keyword):
    tripnameL, fromL, toL, tripViews, userid, image = ([] for i in range(6))
    page_string = request.args.get('page')
    trips = alternateSearchResult(keyword).paginate(int(page_string), POSTS_PER_PAGE, False)

    # since a query result cant be jsonify directly, it shall be assign to different lists
    for trip in trips.items:
        tripnameL.append(trip.tripName)
        fromL.append(trip.tripDateFrom)
        toL.append(trip.tripDateTo)
        tripViews.append(trip.viewsNum)
        userid.append(str(trip.userID))
        image.append(trip.img_thumbnail)

    # sends jsonify objects to the corresponding ajax funciton
    return jsonify(result1=tripnameL, 
                    result2=fromL, 
                    result3=toL, 
                    result4=tripViews, 
                    result5=image, 
                    result6=userid,
                   size=len(tripnameL))


# this route is for the viewing of all iteneraries in one trip
@landing_blueprint.route('/view/<Tripname>', methods=['GET', 'POST'])
def mock(Tripname):
    trips = Trips.query.filter_by(tripName=Tripname).first()
    if trips:
        if trips.status == 1 and trips.visibility == 0:
            # this will increment the given views num of a trip
            trips.viewsNum = trips.viewsNum + 1

            user = User.query.filter_by(id=trips.userID).first()
            itern = Itineraries.query.filter_by(tripID=trips.tripID).all()

            # this will be used for suggestion tab in the template
            all_trips = Trips.query.filter_by(userID=user.id).limit(4)

            db.session.add(trips)
            db.session.commit()
            return render_template('view_trip.html', 
                                    title=trips.tripName, 
                                    trips=trips, 
                                    label=verify(),
                                    ite=itern, 
                                    user=user, 
                                    ph_1=determine_pic(user, 0), 
                                    suggestedTrips=all_trips,
                                    collide=True)

    return render_template('notPermitted.html', 
                            label=verify(), 
                            title='Not Permitted', 
                            collide=True)


# this pagination route is used for the trips that are previed at the landing page
@landing_blueprint.route('/paginate/<int:index>')
def paginate(index):
    tripnameL, fromL, toL, tripViews, userid, image = ([] for i in range(6))
    determiner = True
    page_string = request.args.get('page')

    # to determine if how many page can be accessed
    if int(page_string) == maxPage:
        determiner = False

    # then it will select which category that it should take effect one
    if index == 1:
        trips = tripBASE().order_by(desc(Trips.tripID)).paginate(int(page_string), 4, False)
    elif index == 3 or index == 2:
        trips = tripBASE().order_by(desc(Trips.viewsNum)).paginate(int(page_string), 4, False)

    # again assigning query objects to different list to enable jsonify function to return the results
    for trip in trips.items:
        tripnameL.append(trip.tripName)
        fromL.append(trip.tripDateFrom)
        toL.append(trip.tripDateTo)
        tripViews.append(trip.viewsNum)
        userid.append(str(trip.userID))
        image.append(trip.img_thumbnail)

    return jsonify(result1=tripnameL, 
                    result2=fromL, 
                    result3=toL, 
                    result4=tripViews, 
                    result5=image, 
                    result6=userid,
                    size=len(tripnameL), 
                    determiner=determiner)


# this route is used for sending mails to the default username for app.config
@landing_blueprint.route('/sendResponse')
def sendMail():
    print 'helo'
    body = "From: %s \n Email: %s \n Message: %s" % (
    request.args.get('name'), request.args.get('email'), request.args.get('body'))
    send_email('TravelPlanner', app.config['MAIL_USERNAME'], [app.config['MAIL_USERNAME']], body)
    return jsonify(sent=True)


# this is a customized pagination route for viewwing trips by category and its search functions
@landing_blueprint.route('/exp/<string:linklabel>')
def paginate_1(linklabel):
    tripnameL, fromL, toL, tripViews, userid, image = ([] for i in range(6))
    page_string = request.args.get('page')

    lbl = ['most-popular', 'newest-trip-plans', 'all trips made in this site']

    # identifies the right category
    if linklabel in lbl:
        for index, r in enumerate(lbl):
            if linklabel == r:
                trips = categoryResult(index, int(page_string))
    # for filter search
    elif linklabel == 'filtered_result':
        # getting the global op1 values
        env_variables = ret_op1()
        for index_1, r_1 in enumerate(lbl):
            # checks if env_variables[0] has a match in lbl
            if env_variables[0] == r_1:
                trips = filterSearchResultHandler(index_1, env_variables[1], env_variables[2]).paginate(int(page_string), POSTS_PER_PAGE, False)

    # for the normal search
    else:
        trips = alternateSearchResult(linklabel).paginate(int(page_string), POSTS_PER_PAGE, False)

    for trip in trips.items:
        tripnameL.append(trip.tripName)
        fromL.append(trip.tripDateFrom)
        toL.append(trip.tripDateTo)
        tripViews.append(trip.viewsNum)
        userid.append(str(trip.userID))
        image.append(trip.img_thumbnail)

    return jsonify(result1=tripnameL, 
                    result2=fromL, 
                    result3=toL, 
                    result4=tripViews, 
                    result5=image, 
                    result6=userid,
                    size=len(tripnameL))


# for viewing trips by category
@landing_blueprint.route('/planned-trips/')
@landing_blueprint.route('/planned-trips/<linklabel>', methods=['GET', 'POST'])
def exp_(linklabel='all trips made in this site'):
    til = linklabel
    trips = alternateSearchResult(str(linklabel)).paginate(1, POSTS_PER_PAGE, False)

    main_count = pageNumberDeterminer(len(alternateSearchResult(linklabel).all()))

    count_ = [max_for_most, max_for_new, len(Trips.query.order_by(Trips.tripID).all())]
    lbl = ['most-popular', 'newest-trip-plans', 'all trips made in this site']

    if linklabel in lbl:
        for index, r in enumerate(lbl):
            if linklabel == r:
                til = tripPlansTitle(index)
                trips = categoryResult(index, 1)
                main_count = pageNumberDeterminer(tripBASE().count())


    elif linklabel == 'filtered_result':
        for index_1, r_1 in enumerate(lbl):
            if request.args.get('option') == r_1:
                trips = filterSearchResultHandler(index_1, str(request.args.get('country')), str(request.args.get('city'))).paginate(1, POSTS_PER_PAGE, False)
                main_count = pageNumberDeterminer(filterSearchResultHandler(index_1, str(request.args.get('country')), str(request.args.get('city'))).count())

        change_val(str(request.args.get('option')), str(request.args.get('country')), str(request.args.get('city')))

        return render_template('exp_newtrip.html',
                                path=0, 
                                title=til, 
                                trips=trips, 
                                label=verify(),
                                search_label=request.args.get('city'), 
                                numm=main_count, 
                                stry=linklabel)


    return render_template('exp_newtrip.html', 
                            path=0, 
                            title=til, 
                            trips=trips, 
                            label=verify(),
                            search_label=til, 
                            numm=main_count, 
                            stry=linklabel, 
                            collide=False)


@landing_blueprint.route('/mockk/<int:num>')
def mokkThis(num):
    trip = Trips.query.filter_by(tripID=num).first()
    trip.status = 1
    trip.visibility = 0
    db.session.add(trip)
    db.session.commit()
    return 'ok'