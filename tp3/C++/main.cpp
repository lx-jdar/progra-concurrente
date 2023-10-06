{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOlsvKLhDy8ycUdnbqQYV4h",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/lx-jdar/progra-concurrente/blob/development/tp3/C%2B%2B/main.cpp\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# TP_1 PARTE 3 C++\n",
        "---\n",
        "Dificultades C++: La dificultad de realizar el código fue sincronizar los hilos para que tomaran las distintas cadenas, una vez distribuidos los parametros, cada hilo debía administrar sus propios set de datos sin causar dificultad sobre el otro.\n",
        "\n",
        "\n",
        "Conclusiones: C++ ofrece una implementación de hilos similar a lenguajes más actuales como Java o C y puede desarrollarse muy performante al contar con librería propias del lenguaje."
      ],
      "metadata": {
        "id": "GTpp9XZWYbCu"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "Creación del Archivo C++"
      ],
      "metadata": {
        "id": "bspFVSMdYj6Z"
      }
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "oNUo1QTEXoV6",
        "outputId": "80c1c4e6-de75-424a-88a0-30605cd4335d"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Writing main.cpp\n"
          ]
        }
      ],
      "source": [
        "%%writefile main.cpp\n",
        "#include<thread>\n",
        "#include<iostream>\n",
        "#include<string>\n",
        "#include<string.h>\n",
        "#include<vector>\n",
        "#include<mutex>\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "#define INICIO_FILA  0\n",
        "#define INICIO_COLUM 0\n",
        "#define ARGU_ERROR false\n",
        "#define ARGU_OK true\n",
        "#define CANT_OK 2\n",
        "#define END_ERROR -1\n",
        "#define END_OK 0\n",
        "#define INICIO 0\n",
        "#define ISMAYUS(X) (X>='A' && X<='Z')\n",
        "#define END_CADENA '\\0'\n",
        "\n",
        "\n",
        "bool CheckArguments( int cantArgu );\n",
        "void ConverToMayus(char* cadena);\n",
        "void Conversion(int cantChars,char* cadena,int* listaEnteros);\n",
        "\n",
        "int main(int argc,char* argv[])\n",
        "{\n",
        "    char* cadena=argv[1];\n",
        "    if( CheckArguments(argc) == ARGU_ERROR )\n",
        "    {\n",
        "        std::cout<<\"Cantidad de Argumentos incorrecta, introduzca una SOLA cadena de texto\"<<std::endl;\n",
        "        return END_ERROR;\n",
        "    }\n",
        "    int longitudCad=strlen(cadena);\n",
        "    int* listaEnteros=(int*)malloc(sizeof(int)*longitudCad);\n",
        "    printf(\"La cadena original es:%s\\n\",cadena);\n",
        "    ConverToMayus(cadena);\n",
        "\n",
        "    std::thread hilo1(Conversion,longitudCad/2,cadena,listaEnteros);\n",
        "    std::thread hilo2(Conversion,longitudCad/2+ longitudCad%2,cadena,listaEnteros);\n",
        "\n",
        "\n",
        "    hilo1.join();\n",
        "    hilo2.join();\n",
        "\n",
        "    std::cout<<\"La clave es:\"<<std::endl;\n",
        "    for(int i=0; i<longitudCad;i++)\n",
        "        printf(\"%2d \",listaEnteros[i]);\n",
        "    free(listaEnteros);\n",
        "    return END_OK;\n",
        "}\n",
        "\n",
        "bool CheckArguments(int cantArgu)\n",
        "{\n",
        "    return (cantArgu == CANT_OK? ARGU_OK : ARGU_ERROR);\n",
        "}\n",
        "\n",
        "void Conversion(int cantChars,char* cadena,int* listaEnteros)\n",
        "{\n",
        "    std::mutex mtx;\n",
        "    int convertidos=0;\n",
        "    int contadorChar=INICIO;\n",
        "    while(cantChars>convertidos)\n",
        "    {\n",
        "        mtx.lock();\n",
        "        if(ISMAYUS(cadena[contadorChar]))\n",
        "        {\n",
        "            listaEnteros[contadorChar]=cadena[contadorChar]-'A'+1;\n",
        "            cadena[contadorChar]='0';\n",
        "            convertidos++;\n",
        "        }\n",
        "        mtx.unlock();\n",
        "        contadorChar++;\n",
        "    }\n",
        "    return;\n",
        "}\n",
        "void ConverToMayus(char* cadena)\n",
        "{\n",
        "    while(*cadena != END_CADENA)\n",
        "    {\n",
        "        if(!ISMAYUS(*cadena))\n",
        "            *cadena = *cadena -'a' + 'A';\n",
        "        cadena++;\n",
        "    }\n",
        "}"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "*Compilacion* del Archivo C++"
      ],
      "metadata": {
        "id": "HyPUfpITYotF"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "!g++ -o main main.cpp"
      ],
      "metadata": {
        "id": "mBa4VPvZYsW4"
      },
      "execution_count": 2,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "Ejecución de distintos ejemplos del Programa en Consola"
      ],
      "metadata": {
        "id": "t4EWPW5FYw1R"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "!./main ekjreoid"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "dBgLIcXgYzPy",
        "outputId": "0c60082d-0bad-4add-b58f-4a5738ffbd32"
      },
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "La cadena original es:ekjreoid\n",
            "La clave es:\n",
            " 5 11 10 18  5 15  9  4 "
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!./main ARboLIto"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "9h8y7viYZKoB",
        "outputId": "94cd9cba-3ecd-4c64-f4b8-e67953fe095b"
      },
      "execution_count": 5,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "La cadena original es:ARboLIto\n",
            "La clave es:\n",
            " 1 18  2 15 12  9 20 15 "
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!./main ARboLItofdsdf"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "O0Ufe6BJY65q",
        "outputId": "1c18bd27-13ec-45bc-dd0e-b6b8df314c56"
      },
      "execution_count": 6,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "La cadena original es:ARboLItofdsdf\n",
            "La clave es:\n",
            " 1 18  2 15 12  9 20 15  6  4 19  4  6 "
          ]
        }
      ]
    }
  ]
}