from models.Grupo import Grupo
import os
import sys
import re
import openpyxl
import pandas as pd
from models.Materia import Materia

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
        return 0
    return round(sum(numeros)/contar_si_es_numeros(numeros), 1)


def contar_si_es_numeros(denominador):
    contador = 0
    for elem in denominador:
        if isinstance(elem, str) and elem.isnumeric():
            pass
        elif isinstance(elem, float):
            contador += 1
    return contador


# Directorio de entrada
in_dir = './in'

# Aspectos a evaluar en al materia
aspectos_a_evaluar = (
    'Área formativa',
    'Evaluación',
    'Participación',
    'Tarea',
    'Conducta'
)

criterios_de_evaluacion_por_materia = {'Educación Socioemocional': ['Parcial', 'Uniforme'],
                                       'Science': ['Área formativa','Evaluación','Participación','Tarea','Conducta']}
encabezado_por_materia = {'Educación Socioemocional':[],
                          'Science':[]}

# Obtener la lista de archivos en el directorio de entrada
file_list = os.listdir(in_dir)

if not file_list:
    print("No se encontraron archivos en el directorio 'in'.")
    salir = input('Asegurate de poner archivos con el formato en el folder in')
    sys.exit()

grupo = Grupo(1, "D")
trimestres = [1, 2, 3, 4]
parciales = [1, 2, 3]
_grupo = None

# Recorrer la lista de archivos y leer cada archivo en un DataFrame
for file in file_list:
    if not file.startswith("~$") and (file.endswith(".xls") or file.endswith(".xlsx")):
        # Construir la ruta completa del archivo
        file_path = os.path.join(in_dir, file)
        file_name = str(file)
        # print(file_name)
        # expresiones regulares para buscar las variables
        # identificar el gruapo materia trimestre parcial desde el nombre del archivo:

        # Leer el archivo de excel para buscar las primeras variables
        df0 = pd.read_excel(file_path, skiprows=4, header=None)
        # agregar la materia:
        nombre_materia = df0.iloc[0, 2]
        for curso in criterios_de_evaluacion_por_materia:
            if curso == nombre_materia:
                materia = grupo.agregar_materia(curso, criterios_de_evaluacion_por_materia[curso])
        # Agregar el numero del parcial:
        texto = df0.iloc[0, 3]
        patron = r"\d+[a-zA-Z]{2}\."
        match = re.search(patron, texto)
        if match:
            parcial_actual = materia.set_parcial(int(match.group(0)[:-3]))

        df1 = pd.read_excel(file_path, skiprows=5, header=None)
        # Cuenta las ocurrencias de cada palabra en el primer row
        counts = df1.iloc[0].value_counts()
        # Sacar los indices dependiendo de las ocurrecias de lo que se califica:
        # tarea participación evaluación "área formativa" conducta
        start = 6
        for aspecto in materia.get_a_evaluar():
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
                alumno.set_calificaciones(materia.nombre,parcial_actual, calificacion)


# llenar los parciales que todavia no se califican
for materia in grupo.get_materias():
    sin_calificaciones = {}
    for aspecto in materia.get_a_evaluar():
        sin_calificaciones[aspecto] = [convert_to_float('nan')]
    diferencia = set(parciales) - set(materia.get_parciales())
    if len(diferencia) > 0:
        for parcial_faltante_de_3 in list(diferencia):
            materia.set_parcial(parcial_faltante_de_3)
            for alumno in grupo.get_alumnos():
                alumno.set_calificaciones(materia.nombre,
                    parcial_faltante_de_3, sin_calificaciones)

# Crear encabezados
encabezados = ['Nombre', 'Área formativa 1', 'Área formativa 2', 'Área formativa 3',
               'Evaluación 1', 'Evaluación 2', 'Evaluación 3',
               'Participación 1', 'Participación 2', 'Participación 3',
               'Tarea 1', 'Tarea 2', 'Tarea 3',
               'Conducta 1', 'Conducta 2', 'Conducta 3',
               'Promedio General']
# Crear un encabezado corto para la impersion en terminal
nuevos_encabezados = []
for encabezado in encabezados:
    if encabezado == 'Nombre':
        # nuevos_encabezados.append('Nombre')
        pass
    else:
        palabras = encabezado.split()
        new_encabezado = ''
        for palabra in palabras:
            if palabra[0]:
                new_encabezado += palabra[0].upper()
        nuevos_encabezados.append(new_encabezado)
# encabezado para el archivo de excel
encabezado_algebrix = ['Estudiante',
                       'Science 1 (Biology) : Área formativa 1 ( 3.3% )', 'Science 1 (Biology) : Área formativa 2 ( 3.3% )', 'Science 1 (Biology) : Área formativa 3 ( 3.4% )',
                       'Science 1 (Biology) : Examen parcial 1 ( 15.0% )', 'Science 1 (Biology) : Examen parcial 2 ( 15.0% )', 'Science 1 (Biology) : Examen parcial 3 ( 15.0% )',
                       'Science 1 (Biology) : Participación 1 ( 10.0% )', 'Science 1 (Biology) : Participación 2 ( 10.0% )', 'Science 1 (Biology) : Participación 3 ( 10.0% )',
                       'Science 1 (Biology) : Tareas 1 ( 5.0% )', 'Science 1 (Biology) : Tareas 2 ( 5.0% )', 'Science 1 (Biology) : Tareas 3 ( 5.0% )',
                       'Science 1 (Biology) : Puntos extra',
                       'Conducta 1', 'Conducta 2', 'Conducta 3']

print('\n\n')
first_column_width = 20
data_column_width = 7
promedio_general = []
# calculas el valor del numeor maximo de caractres para la columna de nombre
first_column_width = max(len(alumno.get_nombre_completo())
                         for alumno in grupo.get_alumnos()) + 3

txt_title = 'Nombre'.ljust(first_column_width)
for title in nuevos_encabezados:
    txt_title += title.ljust(data_column_width)
for materia in grupo.get_materias():
    print(f"\tGrupo: {grupo.get_grupo()} Materia: {materia.nombre}\n")
    print(f"")
    print(f"{txt_title}")
    for alumno in grupo.get_alumnos():
        alumno_calificaciones = ''
        for aspecto in materia.get_a_evaluar():
            for indice in materia.get_parciales():
                lista = alumno.get_calificaciones()[indice - 1]
                if isinstance(promedio(lista[materia.nombre][aspecto]), float):
                    alumno_calificaciones += str(
                        promedio(lista[aspecto])).ljust(data_column_width)
                    promedio_general.append(promedio(lista[materia.nombre][aspecto]))
                else:
                    alumno_calificaciones += str('').ljust(data_column_width)
        print(
            f"{alumno.get_nombre_completo().ljust(first_column_width)}{alumno_calificaciones}{promedio(promedio_general)}")
    print('\n\n')
# #calificaciones pro alumno
# for alumno in grupo.get_alumnos():
#     print(f"\n{alumno.get_nombre_completo()}")
#     for calificacion in alumno.get_calificaciones():
#         for parcial in calificacion:
#             print(f"\t{parcial}: {calificacion[parcial]}")


for materia in grupo.get_materias():
    ws.append(encabezado_algebrix)
    for alumno in grupo.get_alumnos():
        fila = [alumno.get_nombre_completo()]
        for aspecto in materia.get_a_evaluar():
            for indice in materia.get_parciales():
                lista = alumno.get_calificaciones()[indice - 1]
                fila.append(promedio(lista[aspecto]))
        fila.insert(13, 0)
        ws.append(fila)
        # Guardar el archivo de Excel
        try:
            wb.save(f"out/{materia.get_nombre()}_calificaciones.xlsx")
            print('Archivo Guardado con exito')
        except Exception as e:
            print("Error\n", str(e))

