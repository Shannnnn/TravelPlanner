from app import app
import os
import unittest
import tempfile

class TripTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def addTrip(self, tripName, tripDateFrom, tripDateTo, tripCity, tripCountry, userID, img_thumbnail, status, visibility, featuredTrip):
        return self.app.post(
            '/trips/createtrip',
            data=dict(tripName=tripName, tripDateFrom=tripDateFrom, tripDateTo=tripDateTo, tripCity=tripCity, tripCountry=tripCountry, userID=userID, img_thumbnail=img_thumbnail, status=status, visibility=visibility, featuredTrip=featuredTrip),
            follow_redirects=True
        )

    def addItinerary(self, itineraryName, itineraryDesc, itineraryLocation, itineraryDate, itineraryTime, tripID, locationTypeID):
        return self.app.post(
            '/trips/<tripName>/additineraries',
            data = dict(itineraryName=itineraryName, itineraryDesc=itineraryDesc, itineraryLocation=itineraryLocation, itineraryDate=itineraryDate, itineraryTime=itineraryTime, tripID=tripID, locationTypeID=locationTypeID),
            follow_redirects=True
        )

    def testViewTripForm(self):
        response = self.app.get('/trips', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def testViewItineraryForm(self):
        response = self.app.get('/trips/tripName/additineraries', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def testAddTrip(self):
        response = self.addTrip('Trip', '1997/01/01', '1997/01/01', 'Iligan City', 'Philippines', 1, '1495638841.png', 0, 1, 0)
        self.assertEqual(response.status_code, 200)

    def testAddItinerary(self):
        response = self.addItinerary('ItnOne', 'ItnDesc', 'ItnLoc', '1997/01/01', '10:00', 1, 1)
        self.assertEqual(response.status_code, 200)

    def testViewTrips(self):
        self.app.post('/createtrip', data=dict(tripName='Trip',
                                               tripDateFrom='10/01/2014',
                                               tripDateTo='10/05/2014',
                                               userID=1,
                                               tripCountry='Philippines',
                                               tripCity='Iligan City',
                                               status=1,
                                               visibility=0,
                                               img_thumbnail='17878h88.jpg',
                                               featuredTrip=0), follow_redirects=True)

        response = self.app.get('/trips', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def testViewItinerary(self):
        self.app.post('/Trip/additineraries', data=dict(itineraryName='west-side',
                                                          itineraryDate='10/01/2014',
                                                          itineraryDesc='area61 here i come!',
                                                          itineraryLocation='Iligan',
                                                          itineraryTime='8:30',
                                                          locationTypeID=1,
                                                          tripID=1), follow_redirects=True)

        response = self.app.get('/trips/Trip/itineraries', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
