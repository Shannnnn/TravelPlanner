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
    itineraryDateFrom = db.Column(db.Date)
    itineraryDateTo = db.Column(db.Date)
    itineraryTimeFrom = db.Column(db.Time)
    itineraryTimeTo = db.Column(db.Time)
    tripID = db.Column(db.Integer, db.ForeignKey("trips.tripID"), nullable=False)

    def __init__(self, itineraryName, itineraryDesc, itineraryDateFrom, itineraryDateTo, itineraryTimeFrom, itineraryTimeTo, tripID):
        self.itineraryName = itineraryName
        self.itineraryDesc = itineraryDesc
        self.itineraryDateFrom = itineraryDateFrom
        self.itineraryDateTo = itineraryDateTo
        self.itineraryTimeFrom = itineraryTimeFrom
        self.itineraryTimeTo = itineraryTimeTo
        self.tripID = tripID

    def __repr__(self):
        return '<itineraryName {}>'.format(self.itineraryName)


