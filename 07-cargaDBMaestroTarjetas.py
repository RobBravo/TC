import pyodbc


print("\nCARGADOR DE BASES DE DATOS - BLACKZERO")
print("------------------------------------")

print("\nCarga de maestro de tarjetas de credito")
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

# 1. Conexión a la base de datos
cnxn = pyodbc.connect(connection_string)

archivo = r'C:\Users\roberto.bravo\Documents\BI\Tarjeta\Maestro\MAESTRO_TARJETAS.txt'

# abrir el archivo de texto y leer sus líneas
with open(archivo, 'r') as f:
    lineas = f.readlines()
    total = len(lineas)
    # mostrar el número de líneas que se van a procesar
    print(f'\nSe van a procesar {len(lineas)} líneas del archivo {archivo}.\n')

    # saltar la primera línea, que son los encabezados de las columnas
    datos = lineas[1:]

    # eliminar todos los registros de la tabla antes de insertar los datos nuevos
    cursor = cnxn.cursor()
    cursor.execute('TRUNCATE TABLE BP.MAESTRO_TARJETAS')
    print("\nSe limpio la tabla con exito")
    # insertar los datos en la tabla
    contador = 0
    for i, linea in enumerate(datos, start=2):
        # separar las columnas en una lista
        valores = linea.split('\t')

        # manejar los valores nulos y vacíos
        valores = [None if valor.strip() == '' or valor.strip() == '0001-01-01' else valor.strip() for valor in valores]

        # construir el comando SQL de inserción
        comando = f"INSERT INTO BP.MAESTRO_TARJETAS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

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

# mostrar mensaje de finalización
print('\nProceso completado correctamente.')