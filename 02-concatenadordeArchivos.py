import os
import sys
from datetime import date
from datetime import timedelta
from TimeMachine import back_time

print("\nCONCATENADOR DE ARCHIVOS - BLACKZERO")
print("------------------------------------")

# Mes en curso 
dias = back_time
hoy = date.today()-timedelta(days=dias)
filedate = str(date.today() - timedelta(days=dias))
anio = filedate[:4]
mes = filedate[5:7]
dia = filedate[8:10]
MesIni = anio + mes 





# Ruta de la carpeta de entrada donde se encuentran los archivos de texto
input_folder = r"C:\Users\roberto.bravo\Documents\BI\Tarjeta\CierreFacturacionHist" + "\\" + MesIni
# Ruta de la carpeta de salida donde se guardará el archivo concatenado
output_folder = r"C:\Users\roberto.bravo\Documents\BI\Tarjeta\CierreFacturacionHist"
if not os.path.exists(input_folder):
    print("\nEl directorio {} no existe. No hay directorios por procesar.".format(input_folder))
    sys.exit()
print("\nA continuacion concatenaran los archivos de la carpeta: ")
print("\n------------------------------------")
print(input_folder)
print("\nA la carpeta ")
print(output_folder)
print("\n------------------------------------")

# Lista para almacenar el contenido de los archivos de texto
contenido_archivos = []

# Recorremos todos los archivos de la carpeta de entrada
for archivo in os.listdir(input_folder):
# Comprobamos que el nombre del archivo comience con 'LISTADO_MOVIMIENTOS_COMBINADO_'
    if archivo.startswith('LISTADO_MOVIMIENTOS_') and archivo.endswith('.txt'):
            print('Procesando archivo:', archivo)
            # Abrimos el archivo y leemos su contenido
            with open(os.path.join(input_folder, archivo), 'r') as f:
                # Leemos todas las líneas del archivo
                lineas = f.readlines()
                # Agregamos todas las líneas menos la primera a la lista
                contenido_archivos.extend(lineas[1:])

    # Unimos el contenido de todos los archivos en un solo string
    contenido_final = ''.join(contenido_archivos)

# Creamos un nuevo archivo con el contenido concatenado en la carpeta de salida
with open(os.path.join(output_folder, 'LISTADO_MOVIMIENTOS_COMBINADO' + '.txt'), 'w') as f:
        f.write(contenido_final)

print("\n------------------------------------")
print('\nSe ha creado el archivo LISTADO_MOVIMIENTOS_COMBINADO' + '.txt')
print('\ncon el contenido concatenado de la carpeta ' + input_folder)
