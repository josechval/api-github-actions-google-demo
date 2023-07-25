"""Tests para la base de datos de la aplicación."""
import pytest
from apiflaskdemo import create_app
from apiflaskdemo.project.models import Alumno, User
from apiflaskdemo.project.schemas import AlumnoSchema
from data.alumnos import data_alumnos


app = create_app()


@pytest.fixture
def base_conectada() -> None:
    """Fixture que conecta a la base de datos y la devuelve"""
    print("Conectando a base de datos...")
    with app.app_context() as conectada:
        print("Base de datos conectada.")
        yield conectada


def test_existe_admin(base_conectada) -> None:
    """Test que comprueba que existe el usuario admin"""
    print("Probando si existe el usuario 'admin...'")
    assert User.query.filter_by(username="admin")
    print("Usuario 'admin' existe.")


def test_existe_tabla_alumnos(base_conectada) -> None:
    """Test que comprueba que existe la tabla alumnos"""
    print('Probando que existan alumnos...')
    assert Alumno.query.all()
    print('Alumnos existen.')
    
    
def test_datos_correctos_alumnos(base_conectada) -> None:
    """Test que comprueba que los datos de los alumnos sean correctos"""
    print('Probando que los datos de los alumnos sean correctos..')
    alumnos_db = Alumno.query.all()
    alumnos_test = [AlumnoSchema().dump(alumno) for alumno in alumnos_db]
    assert alumnos_test == data_alumnos
    print('Datos de los alumnos son correctos.')