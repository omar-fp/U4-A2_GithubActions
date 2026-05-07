-- 1. Cobertura de Pruebas
El entorno de pruebas está dividido en tres módulos principales para garantizar el correcto funcionamiento de las distintas capas de la aplicación:

- test_models.py: Verifica la capa de acceso a datos utilizando SQLAlchemy. Se prueba la creación y persistencia de objetos del modelo Juego.

- test_routes.py: Utiliza el cliente de pruebas de Flask para verificar la accesibilidad de las vistas. Comprueba que las rutas públicas devuelvan un código HTTP 200, y asegura que las rutas protegidas bloqueen el acceso a usuarios no autenticados (código HTTP 302 y redirección a /auth/login).

- test_api.py: Valida los endpoints de la API consumidos en formato JSON. Se insertan datos de prueba en la fase setUp y se verifica que una petición GET a /api/juegos retorne un código 200 y una estructura de datos tipo lista válida.

-- 2. Retos encontrados y soluciones

- Reto 1: Errores de compatibilidad con el código brindado.
Al contar con un constructor 
Solución: 

- Reto 2: Incompatibilidad de arquitectura en las pruebas:
 Al intentar ejecutar los scripts de prueba originales, el sistema arrojó el error ImportError: cannot import name "create_app". Esto ocurrió porque los tests solicitados asumían el uso del patrón avanzado "Application Factory", mientras que el proyecto fue hecho utilizando una instancia global de Flask app = Flask(__name__).
 Solución: Se refactorizaron los archivos de la carpeta tests/. Se importó la instancia global directamente y se inyectó el contexto de la aplicación mediante app.app_context().push() dentro del método setUp(). Además, para garantizar la seguridad de la base de datos real (MySQL) al prescindir de una base de datos en memoria, se eliminó la instrucción db.drop_all()y se diseñó un sistema de limpieza en el método tearDown() que elimina los datos temporales insertados durante cada prueba.

- Reto 3: Error de autenticación en la conexión a la base de datos durante las pruebas.
Al ejecutar el código ya modificado se mostró una ventana de error de acceso, esto debido a que tengo 2 lineas de codigo de conexión dentro de mi app.py por temas de configuración en mis dispositivos en el XAMPP
Solución: Se identificó que el entorno de pruebas estaba intentando acceder a MySQL utilizando una configuración sin contraseña, la cual no coincidía con el entorno local actual (laptop). Se resolvió comentando y descomentando dinámicamente la variable.



-- U4 - A2 Integración Continua con GitHub Actions

![CI](https://github.com/omar-fp/U4-A2_GithubActions/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/github/omar-fp/u4-a2_githubactions/graph/badge.svg?token=BTS04YKA2I)](https://codecov.io/github/omar-fp/u4-a2_githubactions)