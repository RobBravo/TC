import pyodbc

# Establece la conexión con la base de datos SQL Server
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=sql03;DATABASE=an_planeacion;Trusted_Connection=yes')

print('Conexion creada con el servidor SQL03')

# Crea un objeto cursor para ejecutar consultas
cursor = cnxn.cursor()

# Ejecuta el stored procedure
print('Se ejecutara el siguiente procedimiento almacenado: SP_ACTUALIZA_MOVIMIENTOS_TC_HIST_X_MCC')
cursor.execute("EXECUTE dbo.SP_ACTUALIZA_MOVIMIENTOS_TC_HIST_X_MCC")
num_filas_afectadas = cursor.rowcount
print(f"Filas insertadas: {num_filas_afectadas}")

# Hacer commit en la base de datos (si es necesario)
cnxn.commit()

# Cierra el cursor y la conexión
cursor.close()
cnxn.close()

print('Proceso finalizado con exito')
