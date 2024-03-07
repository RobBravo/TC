import subprocess


print('ORQUESTADOR DE CARGA - CUENTAS CANCELADAS')
print('---------------------------------------------')


subprocess.run(['python', '10-CargaCuentasCanceladas.py'])
subprocess.run(['python', '11-concatenadorCuentasCanceladas.py'])
subprocess.run(['python', '12-CargaBDCuentasCanceladas.py'])

