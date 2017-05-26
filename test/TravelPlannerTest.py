import unittest

class TestTravePlanner(unittest.TestCase):
    def setUp(self):
        self.db_fb, travelplanner.app.config['DATABASE'] = tempfile.mkstemp()
        travelplanner.app.config['TESTING'] = True
        self.app = travelplanner.app.test_client()
        with travelplanner.app.app_context():
            travelplanner.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlike(travelplanner.app.config['DATABASE'])


if __name__ == '__main__':
    unittest.main()
