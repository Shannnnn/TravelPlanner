import os
from flask import json
from app import app, mail
import unittest
import tempfile

class TestTravePlanner(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        mail.init_app(app)

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_main_page(self):
        response = self.app.get('/main', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/main/index', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.app.get('/main/about', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/main/about/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_response_page(self):
        response = self.app.get('/main/response', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/main/response/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_response_page_send_request(self):
        self.app.get('/main/response', follow_redirects=True)
        response = self.app.get('/main/sendResponse', data=dict(subject='Welcome Message',sender='travelplannerSy@gmail.com', recipients=['travelplannerSy@gmail.com', 'earlmarkbarangot@gmail.com'], text_body='hello'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'True', str((json.loads(response.data.decode('utf-8')))["sent"]))

    def test_site_search(self):
        self.app.post('/createtrip', data=dict(tripName='area61',
                             tripDateFrom='10/01/2014',
                             tripDateTo='10/05/2014',
                             userID=1,
                             tripCountry='Philippines',
                             tripCity='Iligan City',
                             status=1,
                             visibility=0,
                             img_thumbnail='17878h88.jpg',
                             featuredTrip=0), follow_redirects=True)

        self.app.post('/area61/additineraries', data=dict(itineraryName='west-side',
                             itineraryDate='10/01/2014',
                             itineraryDesc='area61 here i come!',
                             itineraryLocation='Iligan',
                             itineraryTime='8:30',
                             locationTypeID=1,
                             tripID=1), follow_redirects=True)

        response = self.app.get('/main/siteSearch', data=dict(num=1, var='area6'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'area6', response.data)


if __name__ == '__main__':
    unittest.main()