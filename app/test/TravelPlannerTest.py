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
        response = self.register('ivanovich', 'patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register!', response.data)

    def test_valid_login_with_registering(self):
        self.register('silversouly', 'gini@gmail.com', 'testpassword', 3)
        response = self.login('silversouly', 'testpassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'logged in', response.data)
        self.assertIn(b'ERROR! Incorrect login credentials', response.data)

    def test_login_logout_with_registering(self):
        self.register('silversoul', 'gin@gmail.com', 'testpassword', 3)
        self.login('silversoul', 'testpassword')
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in', response.data)

    def test_login_without_registering(self):
        response = self.login('userexpress', 'itsawesome')
        self.assertIn(b'ERROR! Incorrect login credentials', response.data)



if __name__ == '__main__':
    unittest.main()