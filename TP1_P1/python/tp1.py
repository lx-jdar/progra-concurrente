import os
import time

FIRST_PROCESS = 'first'
PROCESS_LIST = 'list'


def create_processes(letter_list, letter = None):
 if letter == None: #Pregunto si es la primera llamada a la funcion para asignar la primera letra
  letter = letter_list.get(FIRST_PROCESS)

 children_pid = []
 if letter in letter_list.get(PROCESS_LIST).keys():#Pregunto si la letra debe tener procesos hijos
  for son_letter in letter_list.get(PROCESS_LIST).get(letter):
   pid = os.fork()
   if pid != 0:
    children_pid.append(pid) #Verdadero, quiere decir que se tiene el valor del pid, lo agrego a la lista
   else:
    create_processes(letter_list, son_letter) #Falso, mando a crear los procesos hijos de la letra
    return

  for child_pid in children_pid:
   os.waitpid(child_pid, 0)

 print(f'My letter is: {letter}. My PID is: {os.getpid()}. My PPID is: {os.getppid()}')
 time.sleep(25)

if __name__ == '__main__':
 letter_list = {FIRST_PROCESS: 'A',PROCESS_LIST: {'A': ['B', 'C'],'B': ['D', 'E'],'C': ['F'], 'E': ['G', 'H'] }}
 create_processes(letter_list)