import unittest
from app import app, db

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_index_access(self):

        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_profile_requires_login(self):
        resp = self.client.get('/agregar_juego')
        self.assertEqual(resp.status_code, 302)

if __name__ == '__main__':
    unittest.main()