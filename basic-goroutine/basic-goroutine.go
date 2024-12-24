package main

import (
	"fmt"
	"time"
)

func printHello() {
	for {
		fmt.Println("Hello")
		time.Sleep(100 * time.Millisecond)
	}
}

func printWorld() {
	for {
		fmt.Println("World")
		time.Sleep(200 * time.Millisecond)
	}
	
	
}

func main() {
	go printHello()
	go printWorld()

	// Allow goroutines to run for 1 seconds
	time.Sleep(1 * time.Second)

	
}