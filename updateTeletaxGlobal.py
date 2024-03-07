import pyodbc
import datetime
import os
import shutil
import subprocess
from welcomeBear import crear_arte_ascii

# Llamas a la función
crear_arte_ascii()

# Obtener el año y el mes actual
now = datetime.datetime.now()
year_month = now.strftime("%Y%m")
# Obtener el primer día del mes actual
first_day_of_month = now.replace(day=1)
# Formatear la fecha en el formato de Access ("YYYYMMDD")
formatted_first_day = first_day_of_month.strftime("%Y%m%d")
print(formatted_first_day)

# Lista de números de extensión
extension_numbers = ('2465','2390','1028','2481','2486','2081','2018','2307','1578','3357','2024','3359','2087','2466','2026','2017','2473','2037','2027','2975','2080','2077','2540','2051','2484','2447','2974','2483','2104','2115','2489','2476','2482','2090','2487','2488','2509','2028','2052','2049','2534','2023','2022','2479','2033','2474','2530','2372','2140')


# Construir el nombre del archivo
file_name = f"LL{year_month}.MDB"

# Ruta completa al archivo de la base de datos origen
db_path_origin = r'\\v00090\Sitios\001\{}'.format(file_name)

print("La ruta del archivo es la siguiente: " + db_path_origin)

# Ruta del directorio destino
destino = r'C:\Users\roberto.bravo\Documents\BI\Tarjeta'

# Copiar el archivo al directorio destino
shutil.copy(db_path_origin, destino)

# Ruta del archivo final
db_path_final = os.path.join(destino, file_name)
print("La ruta final del archivo es la siguiente: " + db_path_final)

# Conexión a la base de datos Access
conn_str = f'DRIVER={{Microsoft Access Driver (*.mdb)}};DBQ={db_path_final};'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Consulta SQL para obtener los datos (ajusta según tus necesidades)
sql_query = f"SELECT * FROM Registros WHERE Fecha_de_Llamada >= '{formatted_first_day}' AND Numero_de_Extension IN {extension_numbers}"
cursor.execute(sql_query)

# Obtener los nombres de las columnas
column_names = [column[0] for column in cursor.description]

# Construir la ruta completa al archivo de salida
output_file = os.path.join(destino, f'datos_exportados_{year_month}.txt')

with open(output_file, 'w') as file:
    # Escribir los nombres de las columnas como encabezados
    file.write('\t'.join(column_names) + '\n')

    # Escribir los datos
    for row in cursor.fetchall():
        file.write('\t'.join(map(str, row)) + '\n')

# Cerrar la conexión
conn.close()

print("Archivo exportando con exito: " + f'datos_exportados_{year_month}.txt')

print("\nCARGADOR DE BASES DE DATOS - BLACKZERO")
print("------------------------------------")

print("\nCarga datos de teletax en el sql03 ")
print("------------------------------------")

# configurar la conexión a la base de datos SQL Server
server = 'sql03'
database = 'an_planeacion'
driver = '{SQL Server}'

# establecer la conexión a la base de datos
connection_string = f"""
    DRIVER={driver};
    SERVER={server};
    DATABASE={database};
     Trusted_Connection=yes;
"""

cnxn = pyodbc.connect(connection_string)

archivo = r'C:\\Users\\roberto.bravo\\Documents\\BI\\Tarjeta\\'+f'datos_exportados_{year_month}.txt'

with open(archivo, 'r') as f:
    lineas = f.readlines()
    total = len(lineas)
    # mostrar el número de líneas que se van a procesar
    print(f'\nSe van a procesar {len(lineas)} líneas del archivo {archivo}.\n')
    # saltar la primera línea, que son los encabezados de las columnas
    datos = lineas[1:]

    # eliminar todos los registros de la tabla antes de insertar los datos nuevos
    cursor = cnxn.cursor()
    cursor.execute('TRUNCATE TABLE an_planeacion.dbo.datos_exportados_teletax_banca_personas')

    print("\nSe limpio la tabla con exito")

    # insertar los datos en la tabla
    contador = 0
    for i, linea in enumerate(datos, start=1):
        # separar las columnas en una lista
        valores = linea.split('\t')

        # manejar los valores nulos y vacíos
        valores = [None if valor.strip() == '' or valor.strip() == '0001-01-01' else valor.strip() for valor in valores]

        # construir el comando SQL de inserción
        comando = f"INSERT INTO an_planeacion.dbo.datos_exportados_teletax_banca_personas VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

         # ejecutar el comando SQL
        try:
            cursor.execute(comando, valores)
        except pyodbc.Error as e: 
            # manejar cualquier error de inversión
            cnxn.rollback()
            errores = str(e).split('\n')
            columna = errores[0].split(' ')[3]
            print(f"Error en la fila {i}: columna {columna} - {e}")
        else:
            cnxn.commit()
            contador += 1
            if contador % 5000 == 0:
                print(f"Filas insertadas: {contador} --- {round(((contador/total)*100),0)}% Completado")
    # mostrar el número total de filas insertadas
    print(f"\nTotal de filas insertadas: {contador}")

# cerrar la conexión a la base de datos
cnxn.close()

# mostrar mensaje de finalización
print('\nProceso completado correctamente.')


print('\n############################################')
subprocess.run(['python', 'RPT_TELETAX.py'])