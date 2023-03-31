from models.Alumno import Alumno
from models.Materia import Materia


class Grupo:
    def __init__(self, grado, letra):
        self.grado = grado
        self.letra = letra
        self.alumnos = []
        self.materias = []

    def agregar_alumno(self, nombre, apellido_paterno, apellido_materno):
        if self.buscar_alumno(nombre, apellido_paterno, apellido_materno) is None:
            alumno = Alumno(nombre, apellido_paterno, apellido_materno)
            self.alumnos.append(alumno)
        else:
            alumno = self.buscar_alumno(nombre, apellido_paterno, apellido_materno)
        return alumno

    def agregar_materia(self, nombre_materia, aspectos_a_evaluar):
        if self.buscar_materia(nombre_materia) is None:
            materia = Materia(nombre_materia, aspectos_a_evaluar)
            self.materias.append(materia)
        else:
            materia = self.buscar_materia(nombre_materia)
        return materia

    def get_alumnos(self):
        return self.alumnos

    def get_materias(self):
        return self.materias
    def get_grupo(self):
        return f'{self.grado}-{self.letra}'

    def buscar_materia(self, nombre_materia):
        for materia in self.materias:
            if materia.nombre == nombre_materia:
                return materia
        return None

    def buscar_alumno(self, nombre, apellido_paterno, apellido_materno):
        for alumno in self.alumnos:
            if alumno.nombre == nombre and alumno.apellido_paterno == apellido_paterno and alumno.apellido_materno == apellido_materno:
                return alumno
        return None
