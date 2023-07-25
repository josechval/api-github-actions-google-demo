from apiflask import APIFlask
from apiflaskdemo.project.models import db, Alumno, User
from apiflaskdemo.project.blueprints import abc_alumnos
from apiflaskdemo.project.auth.blueprints import auth_bp
from sqlalchemy import inspect
from data.alumnos import data_alumnos as alumnos

def create_app():
    '''Función principal de la aplicación'''
    # Crear el objeto app
    app = APIFlask(__name__)
    
    # Obtener la configuración de la aplicación a partir de settings.py
    app.config.from_pyfile("settings.py")
    
    # Se incializa la conexión entre SQLALchemy y la base de datos
    db.init_app(app) 
    
    if app.config["TESTING"]:
        with app.app_context():
            # Elimina la base de datos si existe
            db.drop_all()
            # Crea la base de datos
            db.create_all()
            # Inserta los datos de prueba
            for alumno in alumnos:
                db.session.add(Alumno(**alumno))
            db.session.commit()
                
            # Verifica que exista el usuario admin y lo crea si no es así 
            if not User.query.filter_by(username="admin").first():
                user = User(username='admin',
                           email='example@example.com',
                           password='admin', 
                           active=True)
                db.session.add(user)
                db.session.commit()
                
    # Registra los blueprints con los endpoints
    app.register_blueprint(abc_alumnos, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    #Regresa la aplicación
    return app