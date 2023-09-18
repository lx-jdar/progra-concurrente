import os
import random
import threading

RANGO_MATRIZ_CUADRADA = 5
RANGO_MINIMO_NUMERO = -32
RANGO_MAXIMO_NUMERO = 32
CANTIDAD_DE_HILOS = RANGO_MATRIZ_CUADRADA

threads = []
matriz_a = [];
matriz_b = [];
matriz_cs = [];
matriz_ch = [];

def main():

    #Creo las matrices
    matriz_a = crear_matriz_nro_aleatorio(RANGO_MATRIZ_CUADRADA);
    matriz_b = crear_matriz_nro_aleatorio(RANGO_MATRIZ_CUADRADA);
    
    #Realizo la suma secuencial
    matriz_cs = sumar_matrices_secuencial(matriz_a,matriz_b);
    #Realizo la suma con hilos
    suma_matrices_hilos(matriz_a, matriz_b);
    
    
    for thread in threads:
        thread.join();


    print("\nMostrando matriz A\n");
    mostrar_matriz(matriz_a);

    print("\nMostrando matriz B\n");
    mostrar_matriz(matriz_b);

    print("\nMostrando matriz secuencial\n");
    mostrar_matriz(matriz_cs);

    print("\nMostrando matriz hilos\n");
    mostrar_matriz(matriz_ch);
    
    comparar_Matrices(matriz_ch, matriz_cs);

    os._exit(0);
    

def sumar_matrices_secuencial(matriz_1, matriz_2):
    matriz_resultado = [];

    for fila in range(len(matriz_1)):
        matriz_resultado.append([]);
        for columna in range(len(matriz_1[0])):
            matriz_resultado[fila].append(matriz_1[fila][columna] + matriz_2[fila][columna]);

    return matriz_resultado;

def suma_matrices_hilos(matriz_1, matriz_2):
    for fila in range(len(matriz_1)):
        thread = threading.Thread(target=suma_fila_hilo, args=(matriz_1,matriz_2,fila));
        thread.start();
        threads.append(thread);

def suma_fila_hilo(matriz_1, matriz_2, fila):
    global matriz_ch;
    matriz_ch.append([]);
    for columna in range(len(matriz_1)):
        matriz_ch[fila].append(matriz_1[fila][columna] + matriz_2[fila][columna]);


def crear_matriz_nro_aleatorio(tamMatriz):
    matriz = [];
    for fila in range(tamMatriz):
        matriz.append([]);
        for columna in range(tamMatriz):
            matriz[fila].append(random.randrange(RANGO_MINIMO_NUMERO,RANGO_MAXIMO_NUMERO + 1));
    return matriz;

def crear_matriz_valor(tamMatriz, valor):
    matriz = [];
    for fila in range(tamMatriz):
        matriz.append([]);
        for columna in range(tamMatriz):
            matriz[fila].append(valor);
    return matriz;


def mostrar_matriz(matriz):
    for fila in range(len(matriz)):
        for columna in range(len(matriz[0])):
            print("\t", matriz[fila][columna], end = " ");
        print();


def comparar_Matrices(matriz_1, matriz_2):
    matrices_iguales = True;
    if len(matriz_1) == len(matriz_2) and len(matriz_1[0]) == len(matriz_2[0]):
        for fila in range(len(matriz_1)):
            for columna in range(len(matriz_1[0])):
                if matriz_1[fila][columna] != matriz_2[fila][columna]:
                    matrices_iguales = False;
                    break;
    else:
        matrices_iguales = False;
        
    if matrices_iguales == True:
        print("\nLas matrices son iguales\n");
    else:
        print("\nLas matrices no son iguales\n");

    print();
    return matrices_iguales;


main()