// Axpy con OpenMP, usando c, ejecutado en Colab.

#include <iostream>
#include <vector>
#include <cstdlib>
#include <sys/time.h>
#include <omp.h>    // Cabecera OpenMP

// ----------------------------------------------------------------------------
// Macros que miden el tiempo.

static double dHashTiempoHistory[3];
static struct timeval tv;

#define TIEMPO_INI( h )      \
   gettimeofday(&tv,NULL);   \
   dHashTiempoHistory[ h ] = tv.tv_sec + tv.tv_usec/1000000.0;


#define TIEMPO_FIN( h )      \
   gettimeofday(&tv,NULL);   \
   dHashTiempoHistory[ h ] = ((tv.tv_sec + tv.tv_usec/1000000.0) - dHashTiempoHistory[ h ]) * 1000; // Devuelvo en milisegundos
#define TIEMPO_GET( h ) dHashTiempoHistory[ h ]

#define HTH_TOTAL         1
#define HTH_AXPY_SEC      2
#define HTH_AXPY_OMP      3

using namespace std;

// ----------------------------------------------------------------------------

void axpy( double alfa, vector<double> &X, vector<double> &Y )
{
  int i;

  #pragma omp parallel for
  for(i=0;i<Y.size();i++)
  {
    Y[i] = alfa * X[i] + Y[i];
  }
}

// ----------------------------------------------------------------------------

int main(int argc, char* argv[])
{
  int i,c;
  TIEMPO_INI( HTH_TOTAL )

  // Leo los parametros.
  if( argc != 4 )
  {
      std::cerr<< " Error en los parametros de indicar: (alfa), (Tamanio vector), (ciclos ejecucion)."<<argc<<std::endl;
      exit( -1 );
  }

  float alfa     = atof( argv[1] );
  int cantidad_N = atoi( argv[2] );
  int ciclos     = atoi( argv[3] );

  // --------------------------------------------
  // Defino la memoria de los vectores.

  vector<double> X( cantidad_N );
  vector<double> Y( cantidad_N );

  for (int i=0;i<X.size();i++)
  {
    X[i] = (rand()/(double)RAND_MAX)*0.73;
    Y[i] = (rand()/(double)RAND_MAX)*0.71;
  }

  // --------------------------------------------
  // Realizo la función Axpy con OpenMP.

  TIEMPO_INI( HTH_AXPY_OMP )

  for(c=0;c<ciclos;c++)
  {
    axpy( alfa, X, Y );
  }

  TIEMPO_FIN( HTH_AXPY_OMP )

  // --------------------------------------------
  // Realizo la función Axpy en forma secuencial.

  omp_set_num_threads(1);

  TIEMPO_INI( HTH_AXPY_SEC )

  for(c=0;c<ciclos;c++)
  {
    axpy( alfa, X, Y );
  }

  TIEMPO_FIN( HTH_AXPY_SEC )

  TIEMPO_FIN( HTH_TOTAL )

 std::cout<<"Valores Reales  :" <<std::endl;
 std::cout<<"Tiempo TOTAL     : "<<TIEMPO_GET(HTH_TOTAL   )<<" [ms]"<<std::endl;
 std::cout<<"Tiempo axpy Sec  : "<<TIEMPO_GET(HTH_AXPY_SEC)<<" [ms]"<<std::endl;
 std::cout<<"Tiempo axpy Omp  : "<<TIEMPO_GET(HTH_AXPY_OMP)<<" [ms]"<<std::endl;
 std::cout<<std::endl;
 std::cout<<"SpeedUp          : (tiempo Secuencial/tiempo paralelo) : "<<TIEMPO_GET(HTH_AXPY_SEC)<<" / "<<TIEMPO_GET(HTH_AXPY_OMP)<<" = "<<TIEMPO_GET(HTH_AXPY_SEC)/TIEMPO_GET(HTH_AXPY_OMP)<<std::endl;
 std::cout<<"Eficiencia       : SpeedUp/nro procesadores            : "<<TIEMPO_GET(HTH_AXPY_SEC)/TIEMPO_GET(HTH_AXPY_OMP)<<" / "<<omp_get_num_procs()<<" = "<<TIEMPO_GET(HTH_AXPY_SEC)/(omp_get_num_procs()*TIEMPO_GET(HTH_AXPY_OMP))<<std::endl;
 std::cout<<"Coste Sec        : nro procesadores*Tiempo             : "<<1<<" * "<<TIEMPO_GET(HTH_AXPY_SEC)<<" = "<<TIEMPO_GET(HTH_AXPY_SEC)<<std::endl;
 std::cout<<"Coste Omp        : nro procesadores*Tiempo             : "<<omp_get_num_procs()<<" * "<<TIEMPO_GET(HTH_AXPY_OMP)<<" = "<<omp_get_num_procs()*TIEMPO_GET(HTH_AXPY_OMP)<<std::endl;
 std::cout<<"Funcion Overhead : Coste Omp - tiempo Secuencial       : "<<omp_get_num_procs()*TIEMPO_GET(HTH_AXPY_OMP)<<" - "<<TIEMPO_GET(HTH_AXPY_SEC)<<" = "<<(omp_get_num_procs()*TIEMPO_GET(HTH_AXPY_OMP))-TIEMPO_GET(HTH_AXPY_SEC)<<std::endl;


 std::cout<<std::endl;
 std::cout<<"Valores Ideal: "<<std::endl;
 TIEMPO_GET(HTH_AXPY_OMP) = TIEMPO_GET(HTH_AXPY_SEC) / omp_get_num_procs();
 std::cout<<"Tiempo axpy Sec  : "<<TIEMPO_GET(HTH_AXPY_SEC)<<" [ms]"<<std::endl;
 std::cout<<"Tiempo axpy Omp  : "<<TIEMPO_GET(HTH_AXPY_OMP)<<" [ms]"<<std::endl;

 std::cout<<"SpeedUp          : (tiempo Secuencial/tiempo paralelo) : "<<TIEMPO_GET(HTH_AXPY_SEC)<<" / "<<TIEMPO_GET(HTH_AXPY_OMP)<<" = "<<TIEMPO_GET(HTH_AXPY_SEC)/TIEMPO_GET(HTH_AXPY_OMP)<<std::endl;
 std::cout<<"Eficiencia       : SpeedUp/nro procesadores            : "<<TIEMPO_GET(HTH_AXPY_SEC)/TIEMPO_GET(HTH_AXPY_OMP)<<" / "<<omp_get_num_procs()<<" = "<<TIEMPO_GET(HTH_AXPY_SEC)/(omp_get_num_procs()*TIEMPO_GET(HTH_AXPY_OMP))<<std::endl;
 std::cout<<"Coste Sec        : nro procesadores*Tiempo             : "<<1<<" * "<<TIEMPO_GET(HTH_AXPY_SEC)<<" = "<<TIEMPO_GET(HTH_AXPY_SEC)<<std::endl;
 std::cout<<"Coste Omp        : nro procesadores*Tiempo             : "<<omp_get_num_procs()<<" * "<<TIEMPO_GET(HTH_AXPY_OMP)<<" = "<<omp_get_num_procs()*TIEMPO_GET(HTH_AXPY_OMP)<<std::endl;
 std::cout<<"Funcion Overhead : Coste Omp - tiempo Secuencial       : "<<omp_get_num_procs()*TIEMPO_GET(HTH_AXPY_OMP)<<" - "<<TIEMPO_GET(HTH_AXPY_SEC)<<" = "<<(omp_get_num_procs()*TIEMPO_GET(HTH_AXPY_OMP))-TIEMPO_GET(HTH_AXPY_SEC)<<std::endl;


}