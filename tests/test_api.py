import unittest, json
from app import app, db
from models import Juego

class APITestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        
        self.juego_prueba = Juego(nombre='Test_API', descripcion='Prueba', precio=10.00)
        db.session.add(self.juego_prueba)
        db.session.commit()

    def tearDown(self):
        db.session.delete(self.juego_prueba)
        db.session.commit()
        self.ctx.pop()

    def test_get_juegos(self):
        resp = self.client.get('/api/juegos')
        data = json.loads(resp.data)
        
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(data, list)

if __name__ == '__main__':
    unittest.main()