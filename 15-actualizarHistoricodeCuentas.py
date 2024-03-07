import pyodbc
import calendar
from datetime import date
from datetime import timedelta
from datetime import datetime
from TimeMachine import back_time

# Mes en curso 
dias = back_time
print("Regresando en el tiempo: " + str(dias) + " Dias")
hoy = date.today()-timedelta(days=dias)
print("Fecha del pasado: " + str(hoy) )
date = str(hoy)
anio = int(date[:4])
mes = int(date[5:7])
dia = int(date[8:10])

fecha = datetime(anio, mes, dia)

# Obtener el último día del mes de la fecha de ejemplo
ultimo_dia_mes = calendar.monthrange(fecha.year, fecha.month)[1]

print("Ultimo dia del mes: " + str(ultimo_dia_mes))

# Crear una nueva fecha con el último día del mes
fecha_proceso = str(datetime(fecha.year, fecha.month, ultimo_dia_mes))
print("Fecha proceso: " + str(fecha_proceso))

# Convertir la fecha a un objeto datetime
fecha_proceso_tmp = datetime.strptime(fecha_proceso, '%Y-%m-%d %H:%M:%S')
print("Fecha proceso formato fecha: " + str(fecha_proceso_tmp))

# Obtener la fecha en formato YYYY-MM-DD
fecha_proceso_final = str(datetime.strftime(fecha_proceso_tmp, '%Y%m%d'))

print('Se ejecuta el proceso para : ',date)
print('Fecha Proceso: ', fecha_proceso_final)

# Establece la conexión con la base de datos SQL Server
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=sql03;DATABASE=an_planeacion;Trusted_Connection=yes')

print('Conexion creada con el servidor SQL03')

# Crea un objeto cursor para ejecutar consultas
cursor = cnxn.cursor()

# Ejecuta el stored procedure
print('Se ejecutara el siguiente procedimiento almacenado: ACTUALIZA_maestro_cuentas_tc_hist')
cursor.execute("EXECUTE dbo.ACTUALIZA_maestro_cuentas_tc_hist @fecha_borrar=?",fecha_proceso_final)
num_filas_afectadas = cursor.rowcount
print(f"Filas insertadas: {num_filas_afectadas}")

# Hacer commit en la base de datos (si es necesario)
cnxn.commit()

# Cierra el cursor y la conexión
cursor.close()
cnxn.close()

print('Proceso finalizado con exito')
