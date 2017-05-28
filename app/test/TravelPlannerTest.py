import os
from app import app
import unittest
import tempfile

class TestTravePlanner(unittest.TestCase):
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
        self.app.get('/register', follow_redirects=True)
        self.register('silversou_ly', 'errorcode@gmail.com', 'testpassword', 3)
        self.app.get('/logout', follow_redirects=True)
        self.app.get('/login', follow_redirects=True)
        self.login('silversou_ly', 'testpassword')
        response = self.app.get('/userprofile/silversou_ly/edit', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'logged in', response.data)

    def test_login_without_registration(self):
        self.app.get('/login', follow_redirects=True)
        response = self.login('userexpress', 'itsawesome')
        self.assertIn(b'ERROR! Incorrect login credentials', response.data)

    def test_login_logout_with_registration(self):
        self.app.get('/register', follow_redirects=True)
        self.register('silversoul', 'gin@gmail.com', 'testpassword', 3)
        self.app.get('/login', follow_redirects=True)
        self.login('silversoul', 'testpassword')
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in', response.data)

    def test_request_passeword_change_via_email(self):
        self.app.get('/register', follow_redirects=True)
        self.register('kimimaru', 'kimi@gmail.com', 'testpassword', 3)
        self.app.get('/reset_request', follow_redirects=True)
        response = self.app.post('/reset_request', data=dict(email='kimi@gmail.com'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Something went wrong!', response.data)


if __name__ == '__main__':
    unittest.main()