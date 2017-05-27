from app import app, db
import unittest


class TestTravePlanner(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:databaseadmin@127.0.0.1:5432/testdb'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def testAddTrip(self):
        response = self.addTrip('Trip', '1997/01/01', '1997/01/01', 'Iligan City', 'Philippines', 1, '1495638841.png', 0, 1, 0)
        self.assertEqual(response.status_code, 200)

    def testAddItinerary(self):
        response = self.addItinerary('ItnOne', 'ItnDesc', 'ItnLoc', '1997/01/01', '10:00', 1, 1)
        self.assertEqual(response.status_code, 200)

    def testViewTrips(self):
        response = self.app.get('/trips')
        self.assertEqual(response.status_code, 200)



    def addTrip(self, tripName, tripDateFrom, tripDateTo, tripCity, tripCountry, userID, img_thumbnail, status, visibility, featuredTrip):
        return self.app.post(
            '/trips/createtrip',
            data=dict(tripName=tripName, tripDateFrom=tripDateFrom, tripDateTo=tripDateTo, tripCity=tripCity, tripCountry=tripCountry, userID=userID, img_thumbnail=img_thumbnail, status=status, visibility=visibility, featuredTrip=featuredTrip),
            follow_redirects=True
        )

    def addItinerary(self, itineraryName, itineraryDesc, itineraryLocation, itineraryDate, itineraryTime, tripID, locationTypeID):
        return self.app.post(
            '/trips/<tripName>/additineraries',
            data = dict(itineraryName=itineraryName, itineraryDesc=itineraryDesc, itineraryLocation=itineraryLocation, itineraryDate=itineraryDate, itineraryTime=itineraryTime, tripID=tripID, locationTypeID=locationTypeID)
            )




if __name__ == '__main__':
    unittest.main()