from models.Grupo import Grupo
import os
import re
import pandas as pd
import openpyxl

# Crear un nuevo archivo de Excel
wb = openpyxl.Workbook()

# Seleccionar la hoja activa
ws = wb.active


def convert_to_float(val):
    try:
        if str(val) == 'nan':
            return int(0)
        elif val == 0 or val == 0.0:
            print(val)
            return (float(val))
        else:
            return float(val)
    except Exception as e:
        print(str(e))
        return float('0.0')


def promedio(numeros):
    if len(numeros) == 1 and numeros[0] == 0:
        return ''
    return round(sum(numeros)/contar_numeros(numeros), 1)


def contar_numeros(denominador):
    contador = 0
    for elem in denominador:
        if isinstance(elem, str) and elem.isnumeric():
            print(elem)
            contador = contador
        elif isinstance(elem, float):
            contador += 1
    return contador


# Directorio de entrada
in_dir = './in'
# Aspectos a evaluar en al materia
aspectos_a_evaluar = ['Tarea', 'Participación',
                      'Evaluación', 'Área formativa', 'Conducta']

# Obtener la lista de archivos en el directorio de entrada
file_list = os.listdir(in_dir)

grupo = Grupo(1, "D")
# materia = Materia('Science', aspectos_a_evaluar)
parciales = [1, 2, 3]
materia = grupo.agregar_materia('Science', aspectos_a_evaluar)

# Recorrer la lista de archivos y leer cada archivo en un DataFrame
for file in file_list:
    if not file.startswith("~$") and (file.endswith(".xls") or file.endswith(".xlsx")):
        # Construir la ruta completa del archivo
        file_path = os.path.join(in_dir, file)
        file_name = str(file)
        df0 = pd.read_excel(file_path, skiprows=4, header=None)
        texto = df0.iloc[0, 3]
        patron = r"\d+[a-zA-Z]{2}\."
        match = re.search(patron, texto)
        if match:
            parcial_int = int(match.group(0)[:-3])
        else:
            parcial_int = None
        # print(parcial_int, texto)
        materia.set_parcial(parcial_int)
        df1 = pd.read_excel(file_path, skiprows=5, header=None)
        # Cuenta las ocurrencias de cada palabra en el primer row
        counts = df1.iloc[0].value_counts()
        # Sacar los indices dependiendo de las ocurrecias de lo que se califica:
        # tarea participación evaluación "área formativa" conducta
        start = 6
        for aspecto in aspectos_a_evaluar:
            end = start + counts.get(aspecto, 0) - 1
            globals()[f"{aspecto}_start"] = start
            start = end + 1
            globals()[f"{aspecto}_end"] = end

        # Leer el archivo en un DataFrame de pandas
        df = pd.read_excel(file_path, skiprows=7, header=None)
        for row in df.itertuples():
            if not pd.isna(row[3]):
                apellido_paterno = row[2]
                if pd.isna(row[3]):
                    nombre = row[4]
                    apellido_materno = ''
                else:
                    nombre = row[4]
                    apellido_materno = row[3]
                # agregar el alumno al grupo
                alumno = grupo.agregar_alumno(
                    nombre, apellido_paterno, apellido_materno)
                # print(alumno.get_nombre_completo())
                calificacion = {}
                for aspecto in materia.get_a_evaluar():
                    globals()[f"{aspecto}"] = [convert_to_float(valor)for valor in row
                                               [globals().get(f'{aspecto}_start', 'Variable no definida'): globals().get(f'{aspecto}_end', 'Variable no definida')]]
                    calificacion[aspecto] = globals().get(aspecto)
                alumno.set_calificaciones(parcial_int, calificacion)

sin_calificaciones = {'Tarea': [0], 'Participación': [
    0], 'Evaluación': [0], 'Área formativa': [0], 'Conducta': [0]}
diferencia = set(parciales) - set(materia.get_parciales())
if len(diferencia) > 0:
    for parcial_faltante_de_3 in list(diferencia):
        materia.set_parcial(parcial_faltante_de_3)
        for alumno in grupo.get_alumnos():
            alumno.set_calificaciones(
                parcial_faltante_de_3, sin_calificaciones)


# Crear encabezados
encabezados = ['Nombre', 'Área formativa 1', 'Área formativa 2', 'Área formativa 3',
               'Evaluación 1', 'Evaluación 2', 'Evaluación 3',
               'Participación 1', 'Participación 2', 'Participación 3',
               'Tarea 1', 'Tarea 2', 'Tarea 3',
               'Conducta 1', 'Conducta 2', 'Conducta 3']

encabezado_algebrix = ['Estudiante',
                       'Science 1 (Biology) : Área formativa 1 ( 3.3% )', 'Science 1 (Biology) : Área formativa 2 ( 3.3% )', 'Science 1 (Biology) : Área formativa 3 ( 3.4% )',
                       'Science 1 (Biology) : Examen parcial 1 ( 15.0% )', 'Science 1 (Biology) : Examen parcial 2 ( 15.0% )', 'Science 1 (Biology) : Examen parcial 3 ( 15.0% )',
                       'Science 1 (Biology) : Participación 1 ( 10.0% )', 'Science 1 (Biology) : Participación 2 ( 10.0% )', 'Science 1 (Biology) : Participación 3 ( 10.0% )',
                       'Science 1 (Biology) : Tareas 1 ( 5.0% )', 'Science 1 (Biology) : Tareas 2 ( 5.0% )', 'Science 1 (Biology) : Tareas 3 ( 5.0% )',
                       'Science 1 (Biology) : Puntos extra',
                       'Conducta 1', 'Conducta 2', 'Conducta 3']


txt_title = ''
for title in encabezados:
    txt_title += f"{title}\t"
print(txt_title)
for alumno in grupo.get_alumnos():
    alumno_calificaciones = ''
    for aspecto in materia.get_a_evaluar():
        for indice in materia.get_parciales():
            lista = alumno.get_calificaciones()[indice - 1]
            alumno_calificaciones = f"{alumno_calificaciones}\t{promedio(lista[aspecto])} "
    print(alumno.get_nombre_completo(), alumno_calificaciones)


ws.append(encabezados)
for alumno in grupo.get_alumnos():
    fila = [alumno.get_nombre_completo()]
    for aspecto in materia.get_a_evaluar():
        for indice in materia.get_parciales():
            lista = alumno.get_calificaciones()[indice - 1]
            fila.append(promedio(lista[aspecto]))
    ws.append(fila)

# Guardar el archivo de Excel
try:
    wb.save(f"out/{materia.get_nombre()}_calificaciones.xlsx")
    print('Archivo Guardado con exito')
except Exception as e:
    print("Error\n", str(e))
