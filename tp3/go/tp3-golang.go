package main

import (
	"fmt"
	"os"
	"strings"
	"sync"
)

const (
	ASCII_START     = 64
	CANT_THREADS    = 2
	CHARS_BY_THREAD = 4
	INIT_VALUE      = 0
)

type CharPackage struct {
	offset int
	chars  string
}

var password []int
var mtx sync.Mutex

func convertirAEntero(chnl chan CharPackage, wg *sync.WaitGroup) {
	defer wg.Done()

	for data := range chnl {
		for idx := INIT_VALUE; idx < len(data.chars); idx++ {
			mtx.Lock()
			password[idx+data.offset] = int(data.chars[idx]) - ASCII_START
			mtx.Unlock()
		}
	}

}

func main() {

	cadena := strings.ToUpper(os.Args[1])
	password = make([]int, len(cadena))
	dataT1 := make(chan CharPackage)
	dataT2 := make(chan CharPackage)

	var wg sync.WaitGroup

	// creo los threads que tratan los caracteres
	wg.Add(CANT_THREADS)
	go convertirAEntero(dataT1, &wg)
	go convertirAEntero(dataT2, &wg)

	cycles := len(cadena) / CHARS_BY_THREAD
	if len(cadena)%CHARS_BY_THREAD != INIT_VALUE {
		cycles++
	}
	start, offset := INIT_VALUE, CHARS_BY_THREAD
	for i := INIT_VALUE; i < cycles; i++ {
		// la logica es delegar de a 4 caracteres a los threads
		if i%2 == INIT_VALUE {
			dataT1 <- CharPackage{start, cadena[start:offset]}
		} else {
			dataT2 <- CharPackage{start, cadena[start:offset]}
		}
		// determinos los sig. 4 chars
		start += CHARS_BY_THREAD
		if offset+CHARS_BY_THREAD < len(cadena) {
			offset += CHARS_BY_THREAD
		} else {
			offset = len(cadena)
		}
	}

	close(dataT1)
	close(dataT2)

	wg.Wait()
	fmt.Println("Cadena Cifrada: ", cadena)
	fmt.Println("Cifrado: ", password)
}
