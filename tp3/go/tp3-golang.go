package main

import (
	"fmt"
	"os"
	"regexp"
	"strings"
	"sync"
)

const (
	ASCII_START     = 64
	CANT_THREADS    = 2
	CHARS_BY_THREAD = 4
	INIT_VALUE      = 0
	WORKER_A        = "A"
	WORKER_B        = "B"
)

type CharPackage struct {
	threadID string
	offset   int
	chars    string
}

var password []int
var mtx sync.Mutex

func convertirAEntero(chnl chan CharPackage, wg *sync.WaitGroup) {
	defer wg.Done()

	data := <-chnl
	cadena := data.chars
	charSize := len(cadena)
	cycles := charSize / CHARS_BY_THREAD
	if charSize%CHARS_BY_THREAD > 0 {
		cycles++
	}
	for cycle := 0; cycle < cycles; cycle++ {
		mtx.Lock()
		startIdx := cycle * CHARS_BY_THREAD
		endIdx := startIdx + CHARS_BY_THREAD

		if endIdx > charSize {
			endIdx = charSize
		}
		fmt.Printf("Worker%s procesando %s\n", data.threadID, cadena[startIdx:endIdx])
		for idx := startIdx; idx < endIdx; idx++ {
			password[idx+data.offset] = int(data.chars[idx]) - ASCII_START
		}
		mtx.Unlock()
	}

}

func displayError() {
	fmt.Println("Use: go run tp3-golang.go WordToCypher")
	fmt.Println("[WordToCypher] debe ser al menos una letra del Abecedario A-Z")
	panic("Programa tp3-golang.go mal REALIZADO!")
}

func main() {

	if len(os.Args) < 2 {
		displayError()
	}
	cadena := strings.ToUpper(os.Args[1])
	matched, _ := regexp.MatchString(`^[A-Z]+$`, cadena)
	if !matched {
		displayError()
	}

	password = make([]int, len(cadena))
	dataT1 := make(chan CharPackage)
	dataT2 := make(chan CharPackage)

	var wg sync.WaitGroup

	// creo los threads que tratan los caracteres
	wg.Add(CANT_THREADS)
	go convertirAEntero(dataT1, &wg)
	go convertirAEntero(dataT2, &wg)

	endChars := len(cadena)
	cantChars := endChars / 2
	fmt.Println("######## Distribucion de cadenas ########")
	fmt.Printf("Worker%s: %s\n", WORKER_A, string(cadena[INIT_VALUE:cantChars]))
	fmt.Printf("Worker%s: %s\n\n", WORKER_B, string(cadena[cantChars:endChars]))
	dataT1 <- CharPackage{WORKER_A, INIT_VALUE, string(cadena[INIT_VALUE:cantChars])}
	dataT2 <- CharPackage{WORKER_B, cantChars, string(cadena[cantChars:endChars])}

	close(dataT1)
	close(dataT2)

	wg.Wait()
	fmt.Println("\nCadena Cifrada: ", cadena)
	fmt.Println("Cifrado: ", password)
}
