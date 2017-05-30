import os
from app import app, db
import unittest
import tempfile

class TestTravelPlanner(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def login(self, username, password):
        return self.app.post('/login', data=dict(username=username,password=password), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def register(self, username, email, password, role_id):
        return self.app.post(
            '/register',
            data=dict(username=username, email=email, password=password, role_id=role_id),
            follow_redirects=True
        )

    def test_main_page(self):
        response = self.app.get('/main', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_user_registration_form_displays(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register!', response.data)

    def test_user_login_form_displays(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in!', response.data)

    def test_valid_registration(self):
        self.app.get('/register', follow_redirects=True)
        self.register('ivanovich', 'patkennedy79@gmail.com', 'FlaskIsAwesome', 3)
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in', response.data)

    def test_valid_login_with_registration(self):
        self.app.get('/logout', follow_redirects=True)
        self.app.get('/register', follow_redirects=True)
        self.register('silversou_ly', 'errorcode@gmail.com', 'testpassword', 3)
        self.app.get('/login', follow_redirects=True)
        self.login('silversou_ly', 'testpassword')
        response = self.app.get('/userprofile/silversou_ly/edit', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_without_registration(self):
        self.app.get('/login', follow_redirects=True)
        response = self.login('userexpress', 'itsawesome')
        self.assertIn(b'user not found', response.data)

    def test_login_logout_with_registration(self):
        self.app.get('/register', follow_redirects=True)
        self.register('silversoul', 'gin@gmail.com', 'testpassword', 3)
        self.app.get('/login', follow_redirects=True)
        self.login('silversoul', 'testpassword')
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in', response.data)

    def test_send_request_passeword_change(self):
        self.app.get('/register', follow_redirects=True)
        self.register('kimimaru', 'kimi@gmail.com', 'testpassword', 3)
        self.app.get('/reset_request', follow_redirects=True)
        response = self.app.post('/reset_request', data=dict(email='kimi@gmail.com'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        
class FlaskTestsLoggedIn(unittest.TestCase):
    """Flask tests with user logged into session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:databaseadin@127.0.0.1:5432/testdb'
        self.client = app.test_client()

        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["current_user"] = {
                    "first_name": "John",
                    "user_id": 1,
                    "num_received_requests": 2,
                    "num_sent_requests": 1,
                    "num_total_requests": 3
                }

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_user_profile(self):
        """Test user profile page."""

        result = self.client.get("/users/1")
        self.assertEqual(result.status_code, 200)
        self.assertIn("John", result.data)

    def test_friends(self):
        """Test friends page."""

        result = self.client.get("/friends")
        self.assertIn("My Friends", result.data)

    def test_friends_search(self):
        """Test friends search results page."""

        result = self.client.get("/friends/search",
                                 data={"user_input": "John"})
        self.assertIn("John Test", result.data)
        
class TestAdmin(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        
    def addusers(self, username, email, password, role_id):
        return self.app.post(
            '/admin/users/create',
            data=dict(username=username, email=email, password=password, role_id=role_id),
            follow_redirects=True
        )

    def testAddUser(self):
        response = self.addusers('user', 'user@gmail.com', 'user123', '3')
        self.assertEqual(response.status_code, 200)
        
    def addlocations(self, countryName, countryCode):
        return self.app.post(
            '/admin/trips/location/new',
            data=dict(countryName=countryName, countryCode=countryCode),
            follow_redirects=True
        )    
    
    def testAddLocations(self):
        response = self.addlocations('Baker Street', '221')
        self.assertEqual(response.status_code, 200)
        
    def addcities(self, cityName, cityCode):
        return self.app.post(
            '/admin/trips/<countryName>/city/add',
            data=dict(cityName=cityName, cityCode=cityCode),
            follow_redirects=True
        )   
    
    def testAddCities(self):
        response = self.addcities('Baker Street', '221')
        self.assertEqual(response.status_code, 200)

    def testViewAdmin(self):
        response = self.app.get('/admin', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def testViewUsers(self):
        self.app.post('/admin/users/add', data=dict(username="User",
                                                    email="user@gmail.com",
                                                    password="user123",
                                                    role_id="3"))
        response = self.app.get('/admin/users', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def testViewLocations(self):
        self.app.post('/admin/trips/location/new', data=dict(contryName="Philippines",
                                                              countryCode="9000"))
        response = self.app.get('/admin/trips/location', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def testViewCities(self):
        self.app.post('/admin/trips/<countryName>/city/add', data=dict(cityName="Cebu",
                                                                       cityCode="9700"))
        response = self.app.get('/admin/trips/<countryName>/city', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
