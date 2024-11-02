class ToDoList:
    def __init__(self):
        # Initializes the ToDoList instance with an empty list of tasks.
        self.tasks = []

    def add_task(self, task):
        # Adds a new task to the list with its completion status set to False.
        self.tasks.append({"task": task, "completed": False})
        print("Added task: {}".format(task))

    def mark_completed(self, index):
        # Marks a task as completed if the index is valid.
        try:
            if self.tasks[index]['completed']:
                print("Task already completed: {}".format(self.tasks[index]['task']))
            else:
                self.tasks[index]['completed'] = True
                print("Marked as completed: {}".format(self.tasks[index]['task']))
        except IndexError:
            print("Invalid task number.")

    def delete_task(self, index):
        # Deletes a task from the list if the index is valid.
        try:
            print("Deleted task: {}".format(self.tasks[index]['task']))
            del self.tasks[index]
        except IndexError:
            print("Invalid task number.")

    def show_tasks(self):
        # Displays all tasks and their completion status.
        if not self.tasks:
            print("No tasks to display!")
        for idx, task in enumerate(self.tasks):
            status = "Done" if task['completed'] else "Pending"
            print("{}) {} [{}]".format(idx + 1, task['task'], status))

def main():
    todo = ToDoList()
    # Dictionary mapping user options to their corresponding actions and descriptions.
    actions = {
        '1': ("Add a task", lambda: todo.add_task(input("Enter the task you want to add: "))),
        '2': ("Mark a task as completed", lambda: todo.mark_completed(int(input("Enter task number to mark as completed: ")) - 1)),
        '3': ("Delete a task", lambda: todo.delete_task(int(input("Enter task number to delete: ")) - 1)),
        '4': ("Show all tasks", todo.show_tasks),
        '5': ("Exit", None)
    }

    while True:
        print("\nOptions:")
        for key in actions:
            print(f"{key}. {actions[key][0]}")
        choice = input("Enter your choice: ")

        if choice == '5':
            # Exits the loop and ends the program.
            print("Exiting...")
            break
        elif choice in actions:
            try:
                # Executes the function associated with the user's choice.
                actions[choice][1]()
            except ValueError:
                # Handles cases where a non-integer is entered for indexes.
                print("Please enter a valid number.")
        else:
            # Handles cases where the choice is outside the defined options.
            print("Invalid choice, please choose a valid option.")

if __name__ == "__main__":
    main()
