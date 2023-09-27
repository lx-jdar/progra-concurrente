package main

import (
	"fmt"
	"os"
	"strings"
	"sync"
)

const (
	LETRA_A      = 65
	CANT_THREADS = 2
)

var password []int
var mtx sync.Mutex

func convertirAEntero(cad string, start int, end int, wg *sync.WaitGroup) {
	defer wg.Done()
	mtx.Lock()
	for i := start; i < end; i++ {
		password[i] = int(cad[i]) - LETRA_A + 1
		// fmt.Printf("Char at %d Index Pos = %c int %d \n", i, cad[i], int(cad[i]))
	}
	mtx.Unlock()
}

func main() {
	if len(os.Args) < 1 {
		fmt.Println("Por favor, proporcione el parametro a cifrar!")
	}
	cadena := os.Args[1]
	password = make([]int, len(cadena))

	var wg sync.WaitGroup
	wg.Add(CANT_THREADS)
	fmt.Println("Analyzing Parte 1!")
	go convertirAEntero(strings.ToUpper(cadena), 0, 4, &wg)
	fmt.Println("Analyzing Parte 2!")
	go convertirAEntero(strings.ToUpper(cadena), 4, len(cadena), &wg)
	wg.Wait()

	fmt.Println("\nPalabra Cifrada:", password)
}
