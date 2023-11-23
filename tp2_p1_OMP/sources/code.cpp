// Hola Mundo desde OpenMP, usando c, ejecutado en Colab.

#include <iostream>
#include <vector>
#include <omp.h>    // Cabecera OpenMP

int main(int argc, char* argv[])
{
  int i,j=0,sum;
  std::cout<<"Inicio..."<<std::endl;

  //-----------------------------------------------------------------------------------------------
  // Region paralela
  #pragma omp parallel
  {
    std::cout<<"Hola mundo!!!... soy el hilo " << omp_get_thread_num()<< ", de "<<  omp_get_num_threads() <<", procesadores "<< omp_get_num_procs()<< std::endl;

    #pragma omp single
    {
      std::cout<<"Hola mundo!!!... soy el hilo " << omp_get_thread_num()<< " uno de muchos."<< std::endl;
    }
    #pragma omp master
    {
      std::cout<<"Hola mundo!!!... soy el hilo maestro: " << omp_get_thread_num()<< std::endl;
    }

    #pragma omp for reduction(+:sum) lastprivate(j)
    for(i=0;i<20;i++)
    {
      #pragma omp atomic
      j = j +1;
      std::cout<<"Hola mundo!!!... soy el hilo " << omp_get_thread_num()<< ", itero para i ."<<i<<", actualizo j "<<j<< std::endl;
    }
  }
  // Region paralela
  //-----------------------------------------------------------------------------------------------

  std::cout<<"Fin..., con j="<<j<<std::endl;
}