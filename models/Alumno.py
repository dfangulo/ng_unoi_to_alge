class Alumno():

    def __init__(self, nombre, apellido_paterno, apellido_materno):
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.calificaciones_por_parcial = []

    def get_nombre_completo(self):
        return f"{self.apellido_paterno} { self.apellido_materno}, {self.nombre}"

    def set_calificaciones(self, parcial, notas):
        if len(self.calificaciones_por_parcial) < parcial:
            self.calificaciones_por_parcial += [{} for _ in range(parcial - len(self.calificaciones_por_parcial))]
        self.calificaciones_por_parcial[parcial - 1].update(notas)


    def get_calificaciones(self):
        return self.calificaciones_por_parcial

