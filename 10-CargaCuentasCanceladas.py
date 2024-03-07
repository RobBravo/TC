import os
import shutil
from datetime import date
from datetime import timedelta
from TimeMachine import back_time

print("\nCOPIADOR DE ARCHIVOS - BLACKZERO")
print("--------------------------------")

# Mes en curso 
dias = back_time
hoy = date.today()
filedate = str(hoy - timedelta(days=dias))
anio = filedate[:4]
mes = filedate[5:7]
dia = filedate[8:10]
fecha = anio + mes 

# Ruta de la carpeta de origen
origen = r"\\192.168.11.102\Reporteria\Otros Servicios\Tecnocom\Reportes_Cierre" + "\\" + fecha

# Ruta de la carpeta de destino
destino = r"C:\Users\roberto.bravo\Documents\BI\Tarjeta\Cancelados"+ "\\" + fecha

print("\nA continuacion copiaremos los archivos de la carpeta: ")
print(origen)
print("\nA la carpeta ")
print(destino)
print("\n")

# Creamos la carpeta de destino si no existe
if not os.path.exists(destino):
    os.makedirs(destino)

# Recorremos la carpeta de origen
for archivo in os.listdir(origen):
    # Si el archivo empieza con "LISTADO_MOVIMIENTOS_"
    if archivo.startswith("CONTRATOS_DE_BAJA_"):
        # Creamos la ruta completa del archivo de origen
        ruta_origen = os.path.join(origen, archivo)
        # Creamos la ruta completa del archivo de destino
        ruta_destino = os.path.join(destino, archivo)
        # Copiamos el archivo de origen al destino
        shutil.copyfile(ruta_origen, ruta_destino)
        # Mostramos el nombre del archivo que se está copiando
        print(f"Copiando {archivo}")

print("\nTODOS LOS ARCHIVOS SE HA COPIADO SATISFACTORIAMENTE")