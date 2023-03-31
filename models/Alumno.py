class Alumno():

    def __init__(self, nombre, apellido_paterno, apellido_materno):
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.calificaciones_por_parcial = []
        self.puntos_extra_trimestre = []

    def get_nombre_completo(self):
        return f"{self.apellido_paterno} { self.apellido_materno}, {self.nombre}"

    def set_calificaciones(self, parcial, notas):
        if len(self.calificaciones_por_parcial) < parcial:
            self.calificaciones_por_parcial += [{} for _ in range(parcial - len(self.calificaciones_por_parcial))]
        self.calificaciones_por_parcial[parcial - 1].update(notas)

    def set_puntos_extra(self,nota):
        self.puntos_extra_trimestre.append(nota)

    def get_calificaciones(self):
        return self.calificaciones_por_parcial
    
    def get_puntos_extra(self):
        print(self.puntos_extra_trimestre)
        if self.puntos_extra_trimestre:
            return sum(self.puntos_extra_trimestre)
        else:
            return 0

        
