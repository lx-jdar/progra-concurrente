# progra-concurrente

El objetivo de este tag es cubrir la parte práctica de programas ejecutado con api MPI.
Contiene la parte básica de interacción de procesos esclavos administrados por un proceso principal que distribuye las actividades en el archivo Ejercicio2.py.
El siguiente archivo mpi_tp4.py se encuentra la actividad que realizan los procesos y se distribuyen el procesamiento de filas de acuerdo a la cantidad de procesos creados para tratar los datos en forma equitativa. Una vez finalizado el procesamiento de todos los procesos, se concentra toda la info y cada proceso informa el dato obtenido resuelto en el programa principal por medio de la operatoria reduce.