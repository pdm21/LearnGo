package main

import "fmt"

func remove_element(some_list []string, index int) []string {
	var new_list []string
	new_list = append(new_list, some_list[:index]...)
	new_list = append(new_list, some_list[index+1:]...)
	return new_list
}

func genloop() {
	var tasks []string
	var loop bool = true
	for loop {
		fmt.Println("Welcome to the To Do List Manager:")
		fmt.Println("1. Add A Task")
		fmt.Println("2. View Tasks")
		fmt.Println("3. Mark Task as Done")
		fmt.Println("4. Exit")
		fmt.Println("===================")

		var option int
		fmt.Scanln(&option)

		if (option == 1) {
			fmt.Print("Enter new task: ")
			var temp_task string
			fmt.Scan(&temp_task)

			tasks = append(tasks, temp_task)
		} else if (option == 2) {
			fmt.Println("Tasks to-do: ", tasks)
		} else if (option == 3) {
			fmt.Println("Current Tasks:")
			for i := 0; i < len(tasks); i++ {
				fmt.Println(i, ": ", tasks[i])
			}
			var temp_task int
			fmt.Scan(&temp_task)
			tasks = remove_element(tasks, temp_task)
			fmt.Println("Updated task list: ", tasks)
		} else {
			loop = false
		}
	}
	
	
}

func main() {
	genloop()
}