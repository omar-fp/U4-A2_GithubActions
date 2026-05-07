import unittest
from app import app, db
from models import Juego 

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        db.session.rollback()
        self.ctx.pop()

    def test_juego_creation(self):
        conteo_inicial = Juego.query.count()

        # Juego de prueba
        j = Juego(nombre='Test_Unitaria', descripcion='Prueba', precio=10.00)
        db.session.add(j)
        db.session.commit()

        # Verificamos que ahora haya 1 juego más
        self.assertEqual(Juego.query.count(), conteo_inicial + 1)

        # Se borra
        db.session.delete(j)
        db.session.commit()

if __name__ == '__main__':
    unittest.main()