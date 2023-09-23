package main

import (
	"fmt"
	"math/rand"
	"sync"
)

const (
	MIN_VAL = -32
	MAX_VAL = 32
)

var matrizCC [5][5]int

func main() {
	matrizA, matrizB := retornarMatrices()
	matrizCS := sumarSecuencial(matrizA, matrizB)

	var wg sync.WaitGroup
	sumarConcurrente(matrizA, matrizB, &wg)
	wg.Wait()

	fmt.Println("#### Valores de Matriz CS #####")
	mostrarMatriz(matrizCS)

	fmt.Println("\n#### Valores de Matriz CC #####")
	mostrarMatriz(matrizCC)

}

func retornarMatrices() ([5][5]int, [5][5]int) {
	var matrizA [5][5]int
	var matrizB [5][5]int
	var randomIntegerwithinRange int
	for i := 0; i < len(matrizA); i++ {
		for j := 0; j < len(matrizA[i]); j++ {
			randomIntegerwithinRange = rand.Intn(MAX_VAL-MIN_VAL) + MIN_VAL
			matrizA[i][j] = randomIntegerwithinRange
			randomIntegerwithinRange = rand.Intn(MAX_VAL-MIN_VAL) + MIN_VAL
			matrizB[i][j] = randomIntegerwithinRange
		}
	}
	fmt.Println("#### Valores de Matriz A #####")
	mostrarMatriz(matrizA)
	fmt.Println("#### Valores de Matriz B #####")
	mostrarMatriz(matrizB)

	return matrizA, matrizB
}

func sumarSecuencial(matrizA [5][5]int, matrizB [5][5]int) [5][5]int {
	var matrizCS [5][5]int
	fmt.Println()
	for i := 0; i < len(matrizA); i++ {
		for j := 0; j < len(matrizA[i]); j++ {
			matrizCS[i][j] = matrizA[i][j] + matrizB[i][j]
		}
	}
	return matrizCS
}

func sumarConcurrente(matrizA [5][5]int, matrizB [5][5]int, wg *sync.WaitGroup) {
	for f := 0; f < 5; f++ {
		wg.Add(1)
		go func(pos int, a *[5]int, b *[5]int) { // ejecuta una rutina go. thread liviano
			defer wg.Done()
			//fmt.Printf("fila %3d \n", pos)	// logs it's running concurrently
			for i, _ := range matrizCC[pos] {
				matrizCC[pos][i] = a[i] + b[i]
			}
		}(f, &matrizA[f], &matrizB[f])
	}

}

func mostrarMatriz(matriz [5][5]int) {
	for _, fila := range matriz {
		for _, elemento := range fila {
			fmt.Printf("%3d ", elemento) // Imprime los índices y el elemento de 'matriz'
		}
		fmt.Println()
	}
}
