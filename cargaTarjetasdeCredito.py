import subprocess
import datetime
import time
import logging

# Configuración de registro
log_file = 'carga_log.txt'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ejecutar_subproceso(nombre_script):
    logging.info(f'Iniciando ejecución del subproceso: {nombre_script}')
    
    start_subprocess_time = time.time()
    subprocess.run(['python', nombre_script])
    end_subprocess_time = time.time()

    tiempo_ejecucion = round(end_subprocess_time - start_subprocess_time, 2)
    logging.info(f'El subproceso {nombre_script} tardó {tiempo_ejecucion} segundos en ejecutarse.')
    logging.info(f'Fin de la ejecución del subproceso: {nombre_script}\n')

if __name__ == "__main__":
    logging.info('ORQUESTADOR DE CARGA - TARJETAS DE CREDITO')
    logging.info('---------------------------------------------')

    start_time = time.time()

    fecha_actual = datetime.datetime.now()
    year, month, day = fecha_actual.year, fecha_actual.month, fecha_actual.day
    logging.info(f"SE EJECUTARA LA CARGA PARA EL DIA: {day}/{month}/{year}\n")

    # Lista de scripts a ejecutar
    scripts = [
        '01-copiarArchivos.py',
        '02-concatenadordeArchivos.py',
        '03-cargaArchivosServer.py',
        '04-cargaMaestrodeCuentas.py',
        '05-cargaDBMaestroCuentas.py',
        '06-cargaMaestrodetarjetas.py',
        '07-cargaDBMaestroTarjetas.py',
        '08-cargaSaldos.py',
        '09-cargaDBSaldosTC.py',
        '14-OrquestadorCuentasCanceladas.py',
        '15-actualizarHistoricodeCuentas.py',
        '16-actualizarHistoricodeSaldos.py',
        '17-actualizarMovimientoTCHistxMCC.py',
        # Agrega los demás scripts según sea necesario
    ]

    for script in scripts:
        ejecutar_subproceso(script)

    end_time = time.time()

    elapsed_time = end_time - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)

    logging.info('\nTODA LA CARGA HA FINALIZADO CORRECTAMENTE!')
    logging.info(f'El Proceso tardó {int(hours)}:{int(minutes)}:{int(seconds)} en ejecutarse.')
