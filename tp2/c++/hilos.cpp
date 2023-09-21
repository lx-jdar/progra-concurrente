#include<thread>
#include<iostream>
#include<string>
#include<vector>
#include<time.h>
#define TAM 5

#define LIM_INF -32
#define LIM_SUP  32

#define INICIO_FILA  0
#define INICIO_COLUM 0

#define EJEC_OK 0
bool sonIguales(int matA[][TAM],int matB[][TAM]);
void llenar_matriz(int mat[][TAM],int limInf, int limSup);
void mostrarMatriz(int mat [][TAM]);
void sumarMatricez(int matC[][TAM],int matA[][TAM], int matB[][TAM]);
void sumarFila(int matC[][TAM],int matA[][TAM],int matB[][TAM],int numFila);
int main()
{
    int matrizA[TAM][TAM];
    int matrizB[TAM][TAM];
    int matrizC[TAM][TAM];
    int matrizC_concurrente[TAM][TAM];


    llenar_matriz(matrizA,LIM_INF,LIM_SUP);
    printf("--------Mostrando Matriz A--------\n\n");
    mostrarMatriz(matrizA);

    printf("\n");

    llenar_matriz(matrizB,LIM_INF,LIM_SUP);
    printf("--------Mostrando Matriz B--------\n\n");
    mostrarMatriz(matrizB);

    printf("\n");
    sumarMatricez(matrizC,matrizA,matrizB);
    printf("--------Mostrando Matriz C suma secuencial MatA + MatB--------\n\n");
    mostrarMatriz(matrizC);

    std::vector<std::thread> hilos;
    int contHilosCreados;


    for( contHilosCreados=INICIO_FILA; contHilosCreados<TAM; contHilosCreados++ )
    {
        hilos.push_back(std::thread(sumarFila,matrizC_concurrente,matrizA,matrizB,contHilosCreados));
    }
    std::this_thread::sleep_for(std::chrono::seconds(10));
    for( contHilosCreados=INICIO_FILA; contHilosCreados<TAM; contHilosCreados++ )
    {
        hilos[contHilosCreados].join();
    }

    printf("\n");
    printf("--------Mostrando Matriz C suma concurrente MatA + MatB--------\n\n");
    mostrarMatriz(matrizC_concurrente);

    std::cout<<"El resultado de la comparcion de matrizC_concurrente y la matrizC (secuencia) es: "<<sonIguales(matrizC,matrizC_concurrente)<<" (1=SON IGUALES 0=SON DISTINTAS)"<<std::endl;

    return EJEC_OK;
}
void llenar_matriz(int mat[][TAM],int limInf, int limSup)
{
    int fila,columna;
    std::this_thread::sleep_for(std::chrono::seconds(1));
    srand(time(NULL));
    for(fila=INICIO_FILA; fila<TAM; fila++)
    {
      for(columna=INICIO_COLUM; columna<TAM; columna++)
      {
         mat[fila][columna]=rand()%(2*(limSup+1))+limInf;
      }
    }
}

void mostrarMatriz(int mat[][TAM])
{
    int fila,columna;

    for(fila=INICIO_FILA; fila<TAM; fila++)
    {
      printf("      ");
      for(columna=INICIO_COLUM; columna<TAM; columna++)
      {
         printf("%3d ",mat[fila][columna]);
      }
      printf("\n");
    }
}
void sumarMatricez(int matC[][TAM],int matA[][TAM], int matB[][TAM])
{
    int fila,columna;
    for(fila=INICIO_FILA; fila<TAM; fila++)
    {
      for(columna=INICIO_COLUM; columna<TAM; columna++)
      {
          matC[fila][columna] = matA[fila][columna] + matB[fila][columna];
      }
    }
}
void sumarFila( int matC[][TAM], int matA[][TAM], int matB[][TAM], int numFila)
{
    int columna;
    for(columna=INICIO_COLUM; columna<TAM; columna++)
    {
       matC[numFila][columna] = matA[numFila][columna] + matB[numFila][columna];
    }
}
bool sonIguales(int matA[][TAM],int matB[][TAM])
{
    int fila;
    int columna;
    for( fila=INICIO_FILA; fila<TAM; fila++)
    {
       for( columna=INICIO_COLUM; columna<TAM; columna++)
       {
         if( matA[fila][columna] !=  matB[fila][columna])
            return false;
       }
    }
    return true;
}
