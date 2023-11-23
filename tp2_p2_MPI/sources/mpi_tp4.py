from mpi4py import MPI
import numpy as np
from IPython.display import display

def main():
  comm = MPI.COMM_WORLD
  numProcesses = comm.Get_size() # numero de procesamientos
  rank = comm.Get_rank()

  count = 5
  sendbuf = None

  if rank == 0:
    print("nro de procesos : {}".format(numProcesses), flush=True)
    sendbuf = np.random.randn(numProcesses, count)
    print()
  else:
    sendbuf = None

  smallerPart = np.empty(count, dtype='float')  # allocate space for result on each process
  comm.Scatter(sendbuf, smallerPart, root=0)
  max = comm.reduce(smallerPart.max(), op=MPI.MAX)
     
  print("Rank {} has data: {}".format(rank+1, smallerPart), flush=True)

  if rank == 0:
    print("\nMaster {} of {} has original array after Scatter: \n{}\n"\
    .format(rank+1, numProcesses, sendbuf), flush=True)
    data = { 'info': max }
  else:
    data = {}
  
  #initiate and complete the broadcast
  data = comm.bcast(data, root=0)

  print("Rank {} got max value: {} ".format(rank+1, data['info']), flush=True)

main()