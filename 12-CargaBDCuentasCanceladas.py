import pyodbc
from datetime import date
from datetime import date
from datetime import timedelta
from TimeMachine import back_time

print("\nCARGADOR DE BASES DE DATOS - BLACKZERO")
print("------------------------------------")

print("\nCarga de cuentas canceldas de tarjeta de credito")
print("------------------------------------")




# 1. Conexión a la base de datos
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=sql03;DATABASE=an_planeacion;Trusted_Connection=yes;')

# 2. Creación de un cursor para ejecutar consultas SQL
cursor = cnxn.cursor()

# 3. Eliminar registros del mes en curso
dias = back_time
ahora = date.today()
hoy = str(ahora - timedelta(days=dias))
anio = hoy[:4]
mes = hoy[5:7]

query_delete = "DELETE FROM an_planeacion.BP.CONTRATOS_DE_BAJA WHERE YEAR(FECHA_BAJA_CUENTA)="+anio+" AND MONTH(FECHA_BAJA_CUENTA)="+mes
cursor.execute(query_delete)
cnxn.commit()

print("\nRegistros previos del mes en curso borrados")
print("------------------------------------")

# 4. Apertura del archivo de texto y lectura de su contenido
carpeta =r'C:\Users\roberto.bravo\Documents\BI\Tarjeta\Cancelados' 
archivo_name = 'LISTADO_CONTRATOS_DE_BAJA_COMBINADO.txt'
final_file_input = carpeta + "\\" + archivo_name

# abrir el archivo de texto y leer sus líneas
with open(final_file_input, 'r') as f:
    lineas = f.readlines()
    total = len(lineas)
    # mostrar el número de líneas que se van a procesar
    print(f'\nSe van a procesar {len(lineas)} líneas del archivo {final_file_input}.\n')

    # saltar la primera línea, que son los encabezados de las columnas
    datos = lineas[0:]

    # insertar los datos en la tabla
    contador = 0
    for i, linea in enumerate(datos, start=1):
        # separar las columnas en una lista
        valores = linea.split('\t')

        # manejar los valores nulos y vacíos
        valores = [None if valor.strip() == '' or valor.strip() == ' ' else valor.strip() for valor in valores]

        # construir el comando SQL de inserción
        comando = f"INSERT INTO BP.CONTRATOS_DE_BAJA VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        # ejecutar el comando SQL
        try:
            cursor.execute(comando, valores)
        except pyodbc.Error as e:
            # manejar cualquier error de inversión
            cnxn.rollback()
            errores = str(e).split('\n')
            columna = errores[0].split(' ')[3]
            print(f"\nError en la fila {i}: columna {columna} - {e}")
        else:
            cnxn.commit()
            contador += 1
            if contador % 1000 == 0:
                print(f"Filas insertadas: {contador} --- {round(((contador/total)*100),0)}% Completado")
    # mostrar el número total de filas insertadas
    print(f"\nTotal de filas insertadas: {contador}")


# 7. Cierre del cursor y la conexión

cnxn.close()

# mostrar mensaje de finalización
print('\nProceso completado correctamente.')