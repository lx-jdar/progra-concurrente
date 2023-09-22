package main

import (
	"fmt"
	"os"
	"syscall"
	"time"
)

var nodes map[string]string = map[string]string{
	"A": "CB", "B": "ED", "C": "F",
	"D": "", "E": "HG", "F": ""}

func fork() (uintptr, error) {
	// fork off the parent process
	ret, ret2, errno := syscall.RawSyscall(syscall.SYS_FORK, 0, 0, 0)
	// failure while forking
	if errno != 0 {
		return uintptr(errno), fmt.Errorf("fork failed with error %s", errno.Error())
	}

	// failure
	if ret2 < 0 {
		return ret2, fmt.Errorf("fork failed with pid %d", ret2)
	}

	return ret, nil
}

func createProcess(letter string) uintptr {
	//fmt.Println("This is the process " + letter)

	for i := 0; i < len(nodes[letter]); i++ {

		id, _ := fork()
		if id == 0 {
			node := string(nodes[letter][i])
			fmt.Printf("PID_Child: %d Padre: %d Node: %s\n", os.Getpid(), os.Getppid(), node)
			if len(nodes[letter]) != 0 {
				createProcess(node)
			}
			time.Sleep(10 * time.Second)
			return id
		}
		time.Sleep(1 * time.Second)
	}

	return 1
}

func main() {
	fmt.Printf("PPID_INIT: %d Padre: %d Node: A\n", os.Getpid(), os.Getppid())
	if createProcess("A") == 1 {
		time.Sleep(10 * time.Second)
	}
}
