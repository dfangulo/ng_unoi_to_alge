class Calificaciones:
    def __init__(self, alumno):
        self.alumno = alumno
        self.calificaciones_por_parcial = {}

    def agregar_calificacion(self, aspecto, parcial, calificacion):
        if parcial not in self.calificaciones_por_parcial:
            self.calificaciones_por_parcial[parcial] = {}
        self.calificaciones_por_parcial[parcial][aspecto] = calificacion

    def get_promedio_por_parcial(self, parcial):
        if parcial not in self.calificaciones_por_parcial:
            return None
        aspectos = self.calificaciones_por_parcial[parcial]
        total = sum(aspectos.values())
        promedio = total / len(aspectos)
        return promedio

    def get_promedios_por_parcial(self):
        promedios = {}
        for parcial in self.calificaciones_por_parcial:
            promedios[parcial] = self.get_promedio_por_parcial(parcial)
        return promedios
