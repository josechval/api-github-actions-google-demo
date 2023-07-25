import pytest
from app import create_app
from apiflaskdemo.project.models import db, Alumno
from apiflaskdemo.project.schemas import AlumnoSchema
from flask import Request
from data.alumnos import data_alumnos

app = create_app()

@pytest.fixture
def client() -> Request:
    """Fixture que crea un cliente para hacer peticiones a la API"""
    with app.test_client() as client:
        yield client


def test_get_alumnos(client) -> None:
    """Test que comprueba que se pueden obtener los alumnos"""
    r = client.get('/api/alumnos/')
    print("Validando que se puedan obtener los alumnos...")
    assert r.status_code == 200
    print("Se pueden obtener los alumnos.")
    print("Validando que los datos de los alumnos sean correctos...")
    alumos_response = [AlumnoSchema().dump(alumno) for alumno in r.json]
    assert alumos_response == data_alumnos
    print("Datos de los alumnos son correctos.")


def test_get_alumno(client) -> None:
    """Test que comprueba que se puede obtener un alumno"""
    r = client.get(f'/api/alumno/{data_alumnos[0]["cuenta"]}')
    print("Validando que se pueda obtener un alumno...")
    assert r.status_code == 200
    print("Se puede obtener un alumno.")
    print("Validando que los datos del alumno sean correctos...")
    alumno_response = AlumnoSchema().dump(r.json)
    assert alumno_response == data_alumnos[0]
    print("Datos del alumno son correctos.")


def test_post_alumno(client) -> None:
    """Test que comprueba que se puede crear un alumno"""
    alumno = {
        "nombre": "Amaranta",
        "primer_apellido": "González",
        "segundo_apellido": "García",
        "carrera": "Arquitectura",
        "semestre": 5,
        "promedio": 9.0,
        "al_corriente": True
    }
    r = client.post('/api/alumno/1234567', json=alumno)
    print("Validando que se pueda crear un alumno...")
    assert r.status_code == 201
    print("Se puede crear un alumno.")
    print("Validando que los datos del alumno creado sean correctos...")
    alumno_response = AlumnoSchema().dump(r.json)
    alumno["cuenta"] = 1234567
    assert alumno_response == alumno
    print("Datos del alumno creado son correctos.")


def test_post_alumno_incorrecto(client) -> None:
    """Test que comprueba que no se puede crear un alumno con un esquema incorrecto"""
    alumno = {
        "nombre": "Amaranta",
        "segundo_apellido": "García",
        "carrera": "Natación",
        "semestre": -4,
        "promedio": 20.0,
        "al_corriente": True
        }
    r = client.post('/api/alumno/1234569', json=alumno)
    print("Validando que no se pueda crear un alumno con un esquema incorrecto...")
    assert r.status_code == 422
    print(r.json)
    print("No se puede crear un alumno con un esquema incorrecto.")


def test_post_cuenta_duplicada(client):
    alumno = {
        "nombre": "Amaranta",
        "primer_apellido": "González",
        "segundo_apellido": "García",
        "carrera": "Arquitectura",
        "semestre": 5,
        "promedio": 9.0,
        "al_corriente": True
    }
    r = client.post('/api/alumno/1234567', json=alumno)
    print("Validando que se pueda crear un alumno...")
    assert r.status_code == 409

def test_put_alumno(client) -> None:
    """Test que comprueba que se puede actualizar un alumno"""
    alumno = {
        "nombre": "Amaranta",
        "primer_apellido": "González",
        "segundo_apellido": "García",
        "carrera": "Arquitectura",
        "semestre": 5,
        "promedio": 9.0,
        "al_corriente": True
    }
    r = client.put('/api/alumno/1234567', json=alumno)
    print("Validando que se pueda actualizar un alumno...")
    assert r.status_code == 200
    print("Se puede actualizar un alumno.")
    print("Validando que los datos del alumno actualizado sean correctos...")
    alumno_response = AlumnoSchema().dump(r.json)
    alumno["cuenta"] = 1234567
    assert alumno_response == alumno
    print("Datos del alumno actualizado son correctos.")


def test_login_required(client) -> None:
    """Test que comprueba que se necesita iniciar sesión para eliminar un alumno"""
    r = client.delete(f'/api/alumno/{data_alumnos[0]["cuenta"]}')
    print("Validando que se necesite iniciar sesión para eliminar un alumno...")
    assert r.status_code == 403
    print("Se necesita iniciar sesión para eliminar un alumno.")

def test_login(client) -> None:
    """Test que comprueba que se puede iniciar sesión"""
    r = client.post('/auth/login', json={"username": "admin", "password": "admin"})
    print("Validando que se pueda iniciar sesión...")
    assert r.status_code == 200
    print("Se puede iniciar sesión.")


def test_login_incorrecto(client) -> None:
    """Test que comprueba que no se puede iniciar sesión con un usuario incorrecto"""
    r = client.post('/auth/login', json={"username": "admin", "password": "incorrecto"})
    print("Validando que no se pueda iniciar sesión con un usuario incorrecto...")
    assert r.status_code == 403
    print("No se puede iniciar sesión con un usuario incorrecto.")


def test_del_alumno(client) -> None:
    """Test que comprueba que se puede eliminar un alumno"""
    r = client.post('/auth/login', json={"username": "admin", "password": "admin"})
    print("Validando que se pueda iniciar sesión...")
    assert r.status_code == 200
    print("Se puede iniciar sesión.")
    r = client.delete(f'/api/alumno/{data_alumnos[0]["cuenta"]}')
    print("Validando que se pueda eliminar un alumno...")
    assert r.status_code == 200
    print("Se puede eliminar un alumno.")
    print("Validando que los datos del alumno eliminado sean correctos...")
    alumno_response = AlumnoSchema().dump(r.json)
    assert alumno_response == data_alumnos[0]
    print("Datos del alumno eliminado son correctos.")


def test_logout(client) -> None:
    """Test que comprueba que se puede cerrar sesión"""
    r = client.post('/auth/login', json={"username": "admin", "password": "admin"})
    print("Validando que se pueda iniciar sesión...")
    assert r.status_code == 200
    print("Se puede iniciar sesión.")
    r = client.get('/auth/logout')
    print("Validando que se pueda cerrar sesión...")
    assert r.status_code == 200
    print("Se puede cerrar sesión.")