package main

import (
	"fmt"
	fork "go-fork"
	"os"
)

func init() {
	fork.RegisterFunc("child", child)
	fork.Init()
}

func child(n int) {
	fmt.Printf("child(%d) pid: %d\n", n, os.Getpid())
}
