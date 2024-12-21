package main

import "fmt"

// practice with scanning and storing user input
func main() {
	fmt.Println("Enter your first name: ")
	var first string
	fmt.Scanln(&first)

	fmt.Println("Enter your last name: ")
	var last string
	fmt.Scanln(&last)

	// printf for formatted output
	fmt.Printf("Your full name: %s %s", first, last)
}