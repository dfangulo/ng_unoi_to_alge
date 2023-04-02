class Alumno():

    def __init__(self, nombre, apellido_paterno, apellido_materno):
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.calificaciones_por_parcial = {}
        self.puntos_extra_trimestre = []
        self.materias = []
        
    def set_parcial(self, parcial):
        self.materias.append(parcial)
        return parcial

    def get_nombre_completo(self):
        return f"{self.apellido_paterno} { self.apellido_materno}, {self.nombre}"

    def set_calificaciones(self, materia, parcial, notas):
        if materia not in self.calificaciones_por_parcial:
            self.calificaciones_por_parcial[materia] = [{} for _ in range(parcial)]
        elif len(self.calificaciones_por_parcial[materia]) < parcial:
            self.calificaciones_por_parcial[materia] += [{} for _ in range(parcial - len(self.calificaciones_por_parcial[materia]))]
        self.calificaciones_por_parcial[materia][parcial - 1].update(notas)

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

        
