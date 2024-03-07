import pyodbc
from welcomeBear import crear_arte_ascii

# Llamas a la función
crear_arte_ascii()

# Establece la conexión con la base de datos SQL Server
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=sql03;DATABASE=an_planeacion;Trusted_Connection=yes')

print('Conexion creada con el servidor SQL03')

# Crea un objeto cursor para ejecutar consultas
cursor = cnxn.cursor()

# Ejecuta el stored procedure
print('Se ejecutara el siguiente procedimiento almacenado: pr_actualizar_seguimiento_mesa_de_control')
cursor.execute("EXEC dbo.pr_actualizar_seguimiento_mesa_de_control")

# Verifica si hay mensajes después de la ejecución
if cursor.messages:
    print("Mensajes del servidor:")
    for mensaje in cursor.messages:
        print(mensaje)

# Hacer commit en la base de datos (si es necesario)
cnxn.commit()

# Cierra el cursor y la conexión
cursor.close()
cnxn.close()

print('Proceso finalizado con exito')

