class Materia:
    def __init__(self, nombre, aspectos):
        self.nombre = nombre
        self.aspectos = aspectos
        self.parciales= []
        
    def get_nombre(self):
        return self.nombre
    
    def get_a_evaluar(self):
        return self.aspectos
    
    def get_parciales(self):
        return self.parciales

    def set_parcial(self, parcial):
        self.parciales.append(parcial)
        return parcial
        
    def promedio(self, numeros):
        return round(sum(numeros)/self.contar_numeros(numeros), 1)
  
    @classmethod
    def contar_numeros(cls,tupla):
        contador = 0
        for elem in tupla:
            if isinstance(elem, str) and elem.isnumeric():
                print(elem)
                contador = contador
            elif isinstance(elem, float):
                contador += 1
        return contador
