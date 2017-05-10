from app import db
# db.create_all()
#
from app.trips.model import itineraryLocationType
#
# name = itineraryLocationType('Restaurant', 'name')
# name2 = itineraryLocationType('Hotel', 'icon2')
#
# db.session.add(name)
# db.session.add(name2)
# db.session.commit()
#
# locationTypes = db.session.query(itineraryLocationType.locationType)
# all = locationTypes.all()
# print all

l = list()
m = list()

locationTypeID = db.session.query(itineraryLocationType.locationTypeID)
locationType = db.session.query(itineraryLocationType.locationType)
for i in locationTypeID:
    l.append(i)
for j in locationType:
    m.append(j)

valuee = zip(l, m)

print valuee