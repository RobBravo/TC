import pyodbc
import os
import win32com.client


print('A continuacion se ejecutara el proceso de actualizacion de Base de Welcome')

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=sql03;DATABASE=an_planeacion;Trusted_Connection=yes')

print('Conexion creada con el servidor SQL03')

# Crea un objeto cursor para ejecutar consultas
cursor = cnxn.cursor()

print('Se ejecutara el siguiente procedimiento almacenado: SP_ACTUALIZA_BASE_TEMPORAL_NUEVOS_WELCOME_CALL')
cursor.execute("EXECute dbo.SP_ACTUALIZA_BASE_TEMPORAL_NUEVOS_WELCOME_CALL")
num_filas_afectadas = cursor.rowcount
print(f"Filas insertadas: {num_filas_afectadas}")
cnxn.commit()
# Cierra el cursor y la conexión
cursor.close()
cnxn.close()
print('Proceso finalizado con exito')

print("Se va a actualizar la base de access con la nuevas tarjetas del dia anterior")
print("Creando instancia")
# Crear una instancia de la aplicación Access
access_app = win32com.client.Dispatch("Access.Application")
# Abrir la base de datos de Access
print("Abriendo base de datos")
access_app.OpenCurrentDatabase(r'C:\Users\roberto.bravo\Documents\BI\Tarjeta\BASES_ACTIVIDAD_TC.accdb')

# Ejecutar la consulta
print("Ejecutando consulta")
consulta_nombre = 'update_nuevos_clientes_welcome_call'
access_app.DoCmd.OpenQuery(consulta_nombre)

# Cerrar la base de datos de Access
print("Cerrando consulta")
access_app.CloseCurrentDatabase()

# Cerrar Access
print("Cerrando conexion")
access_app.Quit()


#Nombre del archivo de base de datos
print("Se van a extraer los datos desde la tabla [RyM BD WELCOME CALL]")
file_name = f"BASES_ACTIVIDAD_TC.accdb"
# Ruta del directorio destino
destino = r'C:\Users\roberto.bravo\Documents\BI\Tarjeta'
db_path_final = os.path.join(destino, file_name)

print("Se exportaran a la carpeta: ",db_path_final)
# Conexión a la base de datos Access
conn_str = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path_final};'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
sql_query = f"SELECT * FROM [RyM BD WELCOME CALL]"
cursor.execute(sql_query)
# Obtener los nombres de las columnas
column_names = [column[0] for column in cursor.description]
# Construir la ruta completa al archivo de salida
output_file = os.path.join(destino, f'datos_exportados_base_welcome_call.txt')
with open(output_file, 'w') as file:
    # Escribir los nombres de las columnas como encabezados
    file.write('\t'.join(column_names) + '\n')

    # Escribir los datos
    for row in cursor.fetchall():
        file.write('\t'.join(map(str, row)) + '\n')

# Cerrar la conexión
conn.close()
print("Archivo exportando con exito: " + f'datos_exportados_base_welcome_call.txt') 

print("\nCARGADOR DE BASES DE DATOS - BLACKZERO")
print("------------------------------------")

print("\nCarga datos de Base Welcome Call en el sql03 ")
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
archivo = r'C:\\Users\\roberto.bravo\\Documents\\BI\\Tarjeta\\'+f'datos_exportados_base_welcome_call.txt'

with open(archivo, 'r') as f:
    lineas = f.readlines()
    total = len(lineas)
    # mostrar el número de líneas que se van a procesar
    print(f'\nSe van a procesar {len(lineas)} líneas del archivo {archivo}.\n')
    # saltar la primera línea, que son los encabezados de las columnas
    datos = lineas[1:]

    # eliminar todos los registros de la tabla antes de insertar los datos nuevos
    cursor = cnxn.cursor()
    cursor.execute('TRUNCATE TABLE an_planeacion.dbo.datos_exportados_base_welcome_call_tmp')

    print("\nSe limpio la tabla con exito")

    # insertar los datos en la tabla
    contador = 0
    for i, linea in enumerate(datos, start=1):
        # separar las columnas en una lista
        valores = linea.split('\t')

        # manejar los valores nulos y vacíos
        valores = [None if valor.strip() == '' or valor.strip() == '0001-01-01' else valor.strip() for valor in valores]

        # construir el comando SQL de inserción
        comando = f"INSERT INTO an_planeacion.dbo.datos_exportados_base_welcome_call_tmp VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

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
            if contador % 500 == 0:
                print(f"Filas insertadas: {contador} --- {round(((contador/total)*100),0)}% Completado")
    # mostrar el número total de filas insertadas
    print(f"\nTotal de filas insertadas: {contador}")

# cerrar la conexión a la base de datos
cnxn.close()

#mostrar mensaje de finalización
print('\nProceso completado correctamente.')

print("Se van a extraer los datos desde la tabla [BD TC a Reactivar]")
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
sql_query = f"SELECT * FROM [BD TC a Reactivar]"
cursor.execute(sql_query)
column_names = [column[0] for column in cursor.description]
output_file = os.path.join(destino, f'datos_exportados_base_reactivacion.txt')
with open(output_file, 'w') as file:
    # Escribir los nombres de las columnas como encabezados
    file.write('\t'.join(column_names) + '\n')

    # Escribir los datos
    for row in cursor.fetchall():
        file.write('\t'.join(map(str, row)) + '\n')
conn.close()
print("Archivo exportando con exito: " + f'datos_exportados_base_reactivacion.txt')

print("\nCARGADOR DE BASES DE DATOS - BLACKZERO")
print("------------------------------------")

print("\nCarga datos de Base de Rectivaciones en el sql03 ")
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
archivo = r'C:\\Users\\roberto.bravo\\Documents\\BI\\Tarjeta\\'+f'datos_exportados_base_reactivacion.txt'

with open(archivo, 'r') as f:
    lineas = f.readlines()
    total = len(lineas)
    # mostrar el número de líneas que se van a procesar
    print(f'\nSe van a procesar {len(lineas)} líneas del archivo {archivo}.\n')
    # saltar la primera línea, que son los encabezados de las columnas
    datos = lineas[1:]

    # eliminar todos los registros de la tabla antes de insertar los datos nuevos
    cursor = cnxn.cursor()
    cursor.execute('TRUNCATE TABLE an_planeacion.dbo.datos_exportados_base_reactivacion_tmp')

    print("\nSe limpio la tabla con exito")

    # insertar los datos en la tabla
    contador = 0
    for i, linea in enumerate(datos, start=1):
        # separar las columnas en una lista
        valores = linea.split('\t')

        # manejar los valores nulos y vacíos
        valores = [None if valor.strip() == '' or valor.strip() == '0001-01-01' else valor.strip() for valor in valores]

        # construir el comando SQL de inserción
        comando = f"INSERT INTO an_planeacion.dbo.datos_exportados_base_reactivacion_tmp VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

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
            if contador % 1000 == 0:
                print(f"Filas insertadas: {contador} --- {round(((contador/total)*100),0)}% Completado")
    # mostrar el número total de filas insertadas
    print(f"\nTotal de filas insertadas: {contador}")

# cerrar la conexión a la base de datos
cnxn.close()

#mostrar mensaje de finalización
print('\nProceso completado correctamente.')

print('A continuacion se ejecutara el proceso de actualizacion de Base de Welcome')

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=sql03;DATABASE=an_planeacion;Trusted_Connection=yes')

print('Conexion creada con el servidor SQL03')

# Crea un objeto cursor para ejecutar consultas
cursor = cnxn.cursor()

print('Se ejecutara el siguiente procedimiento almacenado: SP_ACTUALIZA_SEGUIMIENTO_BASES_DE_RETENCIONES_TC')
cursor.execute("EXECute dbo.SP_ACTUALIZA_SEGUIMIENTO_BASES_DE_RETENCIONES_TC")
num_filas_afectadas = cursor.rowcount
print(f"Filas insertadas: {num_filas_afectadas}")
cnxn.commit()
# Cierra el cursor y la conexión
cursor.close()
cnxn.close()
print('Proceso finalizado con exito')


