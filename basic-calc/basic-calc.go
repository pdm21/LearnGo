package main

import "fmt"

func main() {
	fmt.Println("Enter the first number: ")
	var first float32
	fmt.Scanln(&first)

	fmt.Println("Enter the second number: ")
	var second float32
	fmt.Scanln(&second)

	fmt.Println("Enter an operation + - * /")
	var operation string
	fmt.Scanln(&operation)

	var result float32
	if (operation == "+") {
		result = first + second
	} else if (operation == "-") {
		result = first - second
	} else if (operation == "*") {
		result = first * second
	} else {
		result = first / second
	}

	fmt.Printf("The result is %f\n", result)
}