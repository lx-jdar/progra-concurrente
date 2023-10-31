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

func createProcesses(letter string) {
	if letter != "A" {
		fmt.Printf("PID_Child: %5d Padre: %5d Node: %s\n", os.Getpid(), os.Getppid(), letter)
	}
	children := make([]uintptr, len(nodes[letter]))
	var node string
	for i := 0; i < len(nodes[letter]); i++ {
		node = string(nodes[letter][i])
		children[i], _ = fork()
		if children[i] == 0 {
			createProcesses(node)
			return
		}
	}
	for child := range children {
		syscall.Wait4(int(child), nil, 0, nil)
	}
	time.Sleep(10 * time.Second)
	return
}

func main() {
	fmt.Printf("PPID_INIT: %5d Padre: %5d Node: A\n", os.Getpid(), os.Getppid())
	createProcesses("A")
}
