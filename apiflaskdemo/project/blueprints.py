from apiflask import APIBlueprint, abort
from apiflaskdemo.project.auth import login_required
from apiflaskdemo.project.models import db, Alumno
from apiflaskdemo.project.schemas import AlumnoSchema, AlumnoInSchema
from marshmallow.exceptions import ValidationError

abc_alumnos = APIBlueprint('abc_alumno', __name__)

@abc_alumnos.get("/alumnos/")
@abc_alumnos.output(AlumnoSchema(many=True))
def vuelca_base():
    return Alumno.query.all()

@abc_alumnos.get("/alumno/<int:cuenta>")
@abc_alumnos.output(AlumnoSchema)
def despliega_alumno(cuenta):
    return Alumno.query.get_or_404(cuenta)

@abc_alumnos.delete("/alumno/<int:cuenta>")
@abc_alumnos.output(AlumnoSchema)
@login_required
def elimina_alumno(cuenta):
    alumno = Alumno.query.get_or_404(cuenta)
    db.session.delete(alumno)
    db.session.commit()
    return alumno
    
@abc_alumnos.post("/alumno/<int:cuenta>")
@abc_alumnos.output(AlumnoSchema, status_code=201)
@abc_alumnos.input(AlumnoInSchema)
def crea_alumno(cuenta, data):
    if Alumno.query.filter_by(cuenta=cuenta).first():
        abort(409)
    else: 
        data["cuenta"] = cuenta
        alumno = Alumno(**AlumnoSchema().load(data))
        db.session.add(alumno)
        db.session.commit()
        return alumno, 201

@abc_alumnos.put("/alumno/<int:cuenta>")
@abc_alumnos.output(AlumnoSchema)
@abc_alumnos.input(AlumnoInSchema)
def sustituye_alumno(cuenta, data):
    alumno = Alumno.query.get_or_404(cuenta)
    db.session.delete(alumno)
    data["cuenta"] = cuenta
    nuevo_alumno = Alumno(**data)
    db.session.add(nuevo_alumno)
    db.session.commit()
    return  nuevo_alumno