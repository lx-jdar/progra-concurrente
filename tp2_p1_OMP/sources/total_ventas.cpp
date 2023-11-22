#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

#define SEED 4
#define LIMIT_INF 0
#define LIMIT_SUP 100
#define DAYS 15


int main(int argc, char* argv[]){
    if(argv[1])
    {
        int count_suc = atoi( argv[1] );
        int ventas_x_sucursal[count_suc][DAYS];
        int total = 0;

        srand(SEED);
        #pragma omp parallel for
        for (int i = 0; i < count_suc; i++)
        {
            for (int j = 0; j < DAYS; j++)
            {
                #pragma omp critical
                {
                  ventas_x_sucursal[i][j] = (rand() % (LIMIT_SUP - LIMIT_INF + 1)) + LIMIT_INF;
                  total+=ventas_x_sucursal[i][j];
                }
            }
        }

        //
        // Completar código faltante
        //
        #pragma omp parallel for
        for (int i = 0; i < count_suc; i++)
        {
            #pragma omp critical
            {
              for (int j = 0; j < DAYS; j++)
              {
                    printf("%d \t", ventas_x_sucursal[i][j]);
              }
              printf("\n");
            }
        }
        
        printf("%d\n", total);
    }
    else
    {
        printf("Por favor, ingrese la cantidad de sucursales");
    }
}
