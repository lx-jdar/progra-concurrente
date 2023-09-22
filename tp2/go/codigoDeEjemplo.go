package main

import (
	"fmt"
	"os"
	"sync"
	"syscall"
)

var nodes map[string]string = make(map[string]string)

func showInfo() {
	for node := range nodes {
		fmt.Println(node, "=>", nodes[node])
	}
}

func fork() (uintptr, error) {
	// fork off the parent process
	ret, ret2, errno := syscall.RawSyscall(syscall.SYS_FORK, 0, 0, 0)
	if errno != 0 {
		return uintptr(errno), fmt.Errorf("fork failed with error %s", errno.Error())
	}

	// failure
	if ret2 < 0 {
		return ret2, fmt.Errorf("fork failed with pid %d", ret2)
	}

	return ret, nil
}

func main() {
	nodes["A"] = "CB"
	nodes["B"] = "ED"
	nodes["C"] = "F"
	nodes["D"] = ""
	nodes["E"] = "HG"
	nodes["F"] = ""
	foo := 4
	bar := 10
	var wg sync.WaitGroup
	id, _ := fork()
	if id == 0 {
		foo++
		fmt.Printf("In child pid: %d with parent: %d\n", os.Getpid(), os.Getppid())
		showInfo()
		os.Exit(0) //finish the process
	} else {
		bar++
		fmt.Printf("In parent pid: %d\n", os.Getpid())
	}
	wg.Wait()

}
