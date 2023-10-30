from mpi4py import MPI
import numpy as np
import time

# --------------------------------------------
# Formulario
Max_tiempo_sleep =   1#@param {type: "slider", min: 1, max: 10}
Min_tiempo_sleep =   0#@param {type: "slider", min: 0, max: 10}
# --------------------------------------------

# --------------------------------------------
# Constantes de comunicacion
WORK_FLAG = 1
END_WORK_FLAG = 2
# --------------------------------------------

def main():
    comm = MPI.COMM_WORLD # Instanciamos el tipo de comunicador a utilizar.
    id = comm.Get_rank()  # Obtenemos el id como atributo del proceso que se ejecuta.

    # Utilizamos el 0 para definir al procesos Maestro, cualquier otro id sera un esclavo.
    if (id == 0) :
        init() # Llamamos funcion init para eventos que requeriremos inicialmente solo 1 vez.
        numProcesses = comm.Get_size()  # Obtenemos el numero de procesos totales ejecutados.
        numTasks = (numProcesses-1)*4 # Se setea el numero de tareas.
        workTimes = generateTasks(numTasks) # Se generan las tareas, en este caso seran
        print("El jefe crea {} horas de descanso de sus empleados:".format(workTimes.size), flush=True)
        print(workTimes, flush=True)
        initWork(comm, workTimes, numProcesses)
    else:
        doWork(comm)

def generateTasks(numTasks):
    #TODO: Cambiar la semilla del random para que se generen efectivamente diferentes numeros.
    np.random.seed(1000)
    return np.random.randint(low=Min_tiempo_sleep, high=Max_tiempo_sleep, size=numTasks)

def init():
  print()
  print("Version MPI4py utilizada: {}".format(MPI.Get_version()), flush=True)
  print()
  print( "------------------------------------", flush=True)
  print( "Sistema de trabajo Suizo:", flush=True)
  print( "------------------------------------", flush=True)
  print()

def initWork(comm, workTimes, numProcesses):
    totalWork = workTimes.size
    workcount = 0
    recvcount = 0

    print("Jefe enviando las tareas iniciales:", flush=True)
    for id in range(1, numProcesses):
        if workcount < totalWork:
            work=workTimes[workcount]
            comm.send(work, dest=id, tag=WORK_FLAG) # Envia mensaje de iniciar trabajo con el dato correspondiente del array.
            workcount += 1
            print("Jefe envia trabajo y {} hs de descanso al empleado {}.".format(work, id), flush=True)
    print( "------------------------------------", flush=True)

    # Mientras haya trabajo, se recibe el resultado de los empleados y se sigue enviando MAS trabajo.
    while (workcount < totalWork) :
        stat = MPI.Status()
        workTime = comm.recv(source=MPI.ANY_SOURCE, status=stat) # Recivimos resultados de los empleados.
        recvcount += 1
        workerId = stat.Get_source() # Obtenemos el identificador del empleado.
        print("Jefe recibe trabajo completado {} del empleado {}.".format(workTime, workerId), flush=True)
        #send next work
        work=workTimes[workcount]
        comm.send(work, dest=workerId, tag=WORK_FLAG)
        workcount += 1
        print("Jefe envia nuevo trabajo y {} hs de descanso al empleado {}.".format(work, workerId), flush=True)

    while (recvcount < totalWork):
        stat = MPI.Status()
        workTime = comm.recv(source=MPI.ANY_SOURCE, status=stat)
        recvcount += 1
        workerId = stat.Get_source()
        print("Jefe recibe trabajo completado {} del empleado {}.".format(workTime, workerId), flush=True)

    for id in range(1, numProcesses):
        comm.send(0, dest=id, tag=END_WORK_FLAG)


def doWork(comm):
    while(True):
        stat = MPI.Status() # Obtiene el estado actual del empleado.
        waitTime = comm.recv(source=0, tag=MPI.ANY_TAG, status=stat) # Obtiene lo enviado por el Jefe.
        print("Soy el empleado con id {}, toca descanzo por {} hs.".format(comm.Get_rank(), waitTime), flush=True)

        if (stat.Get_tag() == END_WORK_FLAG):
            print("Marca tarjeta el empleado {}.".format(comm.Get_rank()), flush=True)
            return
        time.sleep(waitTime)
        comm.send(waitTime, dest=0)

main()