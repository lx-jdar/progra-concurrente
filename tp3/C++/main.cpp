#include<thread>
#include<iostream>
#include<string>
#include<string.h>
#include<vector>
#include<mutex>




#define INICIO_FILA  0
#define INICIO_COLUM 0
#define ARGU_ERROR false
#define ARGU_OK true
#define CANT_OK 2
#define END_ERROR -1
#define END_OK 0
#define INICIO 0
#define ISMAYUS(X) (X>='A' && X<='Z')
#define END_CADENA '\0'


bool CheckArguments( int cantArgu );
void ConverToMayus(char* cadena);
void Conversion(int cantChars,char* cadena,int* listaEnteros);

int main(int argc,char* argv[])
{
    char* cadena=argv[1];
    if( CheckArguments(argc) == ARGU_ERROR )
    {
        std::cout<<"Cantidad de Argumentos incorrecta, introduzca una SOLA cadena de texto"<<std::endl;
        return END_ERROR;
    }
    int longitudCad=strlen(cadena);
    int* listaEnteros=(int*)malloc(sizeof(int)*longitudCad);
    printf("La cadena original es:%s\n",cadena);
    ConverToMayus(cadena);

    std::thread hilo1(Conversion,longitudCad/2,cadena,listaEnteros);
    std::thread hilo2(Conversion,longitudCad/2+ longitudCad%2,cadena,listaEnteros);


    hilo1.join();
    hilo2.join();

    std::cout<<"La clave es:"<<std::endl;
    for(int i=0; i<longitudCad;i++)
        printf("%2d ",listaEnteros[i]);
    free(listaEnteros);
    return END_OK;
}

bool CheckArguments(int cantArgu)
{
    return (cantArgu == CANT_OK? ARGU_OK : ARGU_ERROR);
}

void Conversion(int cantChars,char* cadena,int* listaEnteros)
{
    std::mutex mtx;
    int convertidos=0;
    int contadorChar=INICIO;
    while(cantChars>convertidos)
    {
        mtx.lock();
        if(ISMAYUS(cadena[contadorChar]))
        {
            listaEnteros[contadorChar]=cadena[contadorChar]-'A'+1;
            cadena[contadorChar]='0';
            convertidos++;
        }
        mtx.unlock();
        contadorChar++;
    }
    return;
}
void ConverToMayus(char* cadena)
{
    while(*cadena != END_CADENA)
    {
        if(!ISMAYUS(*cadena))
            *cadena = *cadena -'a' + 'A';
        cadena++;
    }
}
