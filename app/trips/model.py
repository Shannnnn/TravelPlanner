from app import db

class Trips(db.Model):
    __tablename__ = "trips"
    tripID = db.Column(db.Integer, primary_key=True)
    tripName = db.Column(db.String(70))
    tripDateFrom = db.Column(db.Date)
    tripDateTo = db.Column(db.Date)
    userID = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    viewsNum = db.Column(db.Integer)
    img_thumbnail = db.Column(db.String(70))
    # status = db.Column(db.Boolean, default=True, nullable=False)
    # visibility = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, tripName, tripDateFrom, tripDateTo, userID, img_thumbnail):
        self.tripName = tripName
        self.tripDateFrom = tripDateFrom
        self.tripDateTo = tripDateTo
        self.userID = userID
        self.viewsNum = 0
        self.img_thumbnail = img_thumbnail

    def __repr__(self):
        return '<tripName {}>'.format(self.tripName)

class Itineraries(db.Model):
    __tablename__ = "itineraries"
    itineraryID = db.Column(db.Integer, primary_key=True)
    itineraryName = db.Column(db.String(70))
    itineraryDesc = db.Column(db.String(1000))
    itineraryLocation = db.Column(db.String(80))
    itineraryDateFrom = db.Column(db.Date)
    itineraryDateTo = db.Column(db.Date)
    itineraryTimeFrom = db.Column(db.Time)
    itineraryTimeTo = db.Column(db.Time)
    tripID = db.Column(db.Integer, db.ForeignKey("trips.tripID"), nullable=False)
    locationTypeID = db.Column(db.Integer, db.ForeignKey("itinerarylocationtype.locationTypeID"), nullable=True)

    def __init__(self, itineraryName, itineraryDesc, itineraryLocation, itineraryDateFrom, itineraryDateTo, itineraryTimeFrom, itineraryTimeTo, tripID, locationTypeID):
        self.itineraryName = itineraryName
        self.itineraryDesc = itineraryDesc
        self.itineraryLocation = itineraryLocation
        self.itineraryDateFrom = itineraryDateFrom
        self.itineraryDateTo = itineraryDateTo
        self.itineraryTimeFrom = itineraryTimeFrom
        self.itineraryTimeTo = itineraryTimeTo
        self.tripID = tripID
        self.locationTypeID = locationTypeID

    def __repr__(self):
        return '<itineraryName {}>'.format(self.itineraryName)

class itineraryLocationType(db.Model):
    __tablename__ = "itinerarylocationtype"
    locationTypeID = db.Column(db.Integer, primary_key=True)
    locationType = db.Column(db.String(20))
    locationTypeIcon = db.Column(db.String(30))

    def __init__(self, locationType, locationTypeIcon):
        self.locationType = locationType
        self.locationTypeIcon = locationTypeIcon

    def __repr__(self):
        return '<locationType {}>'.format(self.locationType)

class tripPhotos(db.Model):
    __tablename__ = "trip_Photos"

    id = db.Column(db.Integer, primary_key=True)
    photoName = db.Column(db.String(300))
    photoDate = db.Column(db.Date)
    photoLocation = db.Column(db.String(300))
    tripID = db.Column(db.Integer, db.ForeignKey("trips.tripID"), nullable=False)

    def __init__(self, photoName, photoDate, photoLocation, tripID):
        self.photoName = photoName
        self.photoDate = photoDate
        self.photoLocation = photoLocation
        self.tripID = tripID

    def __repr__(self):
        return '<photoName {}>'.format(self.photoName)