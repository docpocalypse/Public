import tkinter as tk
from tkinter import messagebox
import random

class Cell:
    def __init__(self, master, x, y, size, game):
        self.master = master
        self.x = x
        self.y = y
        self.size = size
        self.game = game
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

        self.button = tk.Button(master, width=2, height=1, command=self.reveal)
        self.button.bind('<Button-3>', self.toggle_flag)  # Right-click to flag
        self.button.grid(row=y, column=x)
    
    def reveal(self):
        if self.is_flagged or self.is_revealed:
            return
        self.is_revealed = True
        if self.is_mine:
            self.button.config(text='💣', bg='red', disabledforeground='black')
            self.game.game_over(False)
        else:
            if self.adjacent_mines > 0:
                self.button.config(
                    text=str(self.adjacent_mines),
                    relief=tk.SUNKEN,
                    state=tk.DISABLED,
                    disabledforeground=self.game.get_color(self.adjacent_mines)
                )
            else:
                self.button.config(relief=tk.SUNKEN, state=tk.DISABLED)
                self.game.reveal_adjacent(self.x, self.y)
            self.game.check_win()
    
    def toggle_flag(self, event):
        if self.is_revealed:
            return
        if not self.is_flagged:
            self.button.config(text='🚩', fg='red')
            self.is_flagged = True
            self.game.flags += 1
        else:
            self.button.config(text='', fg='black')
            self.is_flagged = False
            self.game.flags -= 1
        self.game.update_flag_label()

class Minesweeper:
    def __init__(self, master, width=10, height=10, mines=10):
        self.master = master
        self.width = width
        self.height = height
        self.mines = mines
        self.flags = 0
        self.cells = {}
        self.game_over_flag = False

        # Adjust the grid to make space for the flag label
        self.flag_label = tk.Label(master, text=f"Flags: {self.flags}/{self.mines}", font=("Arial", 14))
        self.flag_label.grid(row=height, column=0, columnspan=width)

        self.create_cells()
        self.place_mines()
        self.calculate_adjacent_mines()
    
    def create_cells(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = Cell(self.master, x, y, 2, self)
                self.cells[(x, y)] = cell
    
    def place_mines(self):
        # Convert dict_keys to list to ensure random.sample works correctly
        mine_positions = random.sample(list(self.cells.keys()), self.mines)
        for pos in mine_positions:
            self.cells[pos].is_mine = True
    
    def calculate_adjacent_mines(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.cells[(x, y)]
                if cell.is_mine:
                    continue
                count = 0
                for nx in range(max(0, x-1), min(self.width, x+2)):
                    for ny in range(max(0, y-1), min(self.height, y+2)):
                        if self.cells[(nx, ny)].is_mine:
                            count += 1
                cell.adjacent_mines = count
    
    def reveal_adjacent(self, x, y):
        for nx in range(max(0, x-1), min(self.width, x+2)):
            for ny in range(max(0, y-1), min(self.height, y+2)):
                cell = self.cells[(nx, ny)]
                if not cell.is_revealed and not cell.is_mine:
                    cell.reveal()
    
    def check_win(self):
        for cell in self.cells.values():
            if not cell.is_mine and not cell.is_revealed:
                return
        self.game_over(True)
    
    def game_over(self, won):
        if self.game_over_flag:
            return
        self.game_over_flag = True
        if won:
            messagebox.showinfo("Minesweeper", "Congratulations! You won!")
        else:
            messagebox.showinfo("Minesweeper", "Game Over! You hit a mine.")
            for cell in self.cells.values():
                if cell.is_mine:
                    cell.button.config(text='💣', bg='red')
        self.master.destroy()
    
    def update_flag_label(self):
        self.flag_label.config(text=f"Flags: {self.flags}/{self.mines}")
    
    def get_color(self, number):
        colors = {
            1: 'blue',
            2: 'green',
            3: 'red',
            4: 'dark blue',
            5: 'brown',
            6: 'cyan',
            7: 'black',
            8: 'grey',
        }
        return colors.get(number, 'black')

class MainMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper - Select Difficulty")
        self.master.geometry("300x200")
        self.create_widgets()
    
    def create_widgets(self):
        title = tk.Label(self.master, text="Minesweeper", font=("Arial", 20))
        title.pack(pady=20)

        btn_beginner = tk.Button(self.master, text="Beginner (9x9, 10 Mines)", width=25, command=lambda: self.start_game(9, 9, 10))
        btn_beginner.pack(pady=5)

        btn_intermediate = tk.Button(self.master, text="Intermediate (16x16, 40 Mines)", width=25, command=lambda: self.start_game(16, 16, 40))
        btn_intermediate.pack(pady=5)

        btn_expert = tk.Button(self.master, text="Expert (30x16, 99 Mines)", width=25, command=lambda: self.start_game(30, 16, 99))
        btn_expert.pack(pady=5)

        btn_custom = tk.Button(self.master, text="Custom", width=25, command=self.custom_settings)
        btn_custom.pack(pady=10)

    def start_game(self, width, height, mines):
        self.master.destroy()  # Close the main menu
        root = tk.Tk()
        root.title("Minesweeper")
        game = Minesweeper(root, width=width, height=height, mines=mines)
        root.mainloop()
    
    def custom_settings(self):
        CustomSettings(self.master)

class CustomSettings:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Custom Settings")
        self.window.geometry("300x250")
        self.create_widgets()
    
    def create_widgets(self):
        title = tk.Label(self.window, text="Custom Settings", font=("Arial", 16))
        title.pack(pady=10)

        # Grid Width
        lbl_width = tk.Label(self.window, text="Grid Width:")
        lbl_width.pack(pady=5)
        self.entry_width = tk.Entry(self.window)
        self.entry_width.pack(pady=5)
        self.entry_width.insert(0, "10")

        # Grid Height
        lbl_height = tk.Label(self.window, text="Grid Height:")
        lbl_height.pack(pady=5)
        self.entry_height = tk.Entry(self.window)
        self.entry_height.pack(pady=5)
        self.entry_height.insert(0, "10")

        # Number of Mines
        lbl_mines = tk.Label(self.window, text="Number of Mines:")
        lbl_mines.pack(pady=5)
        self.entry_mines = tk.Entry(self.window)
        self.entry_mines.pack(pady=5)
        self.entry_mines.insert(0, "10")

        # Start Button
        btn_start = tk.Button(self.window, text="Start Game", command=self.validate_and_start)
        btn_start.pack(pady=20)
    
    def validate_and_start(self):
        try:
            width = int(self.entry_width.get())
            height = int(self.entry_height.get())
            mines = int(self.entry_mines.get())

            if width <= 0 or height <= 0 or mines <= 0:
                raise ValueError

            if mines >= width * height:
                messagebox.showerror("Invalid Input", "Number of mines must be less than total cells.")
                return

            self.window.destroy()
            self.parent.destroy()  # Close the main menu
            root = tk.Tk()
            root.title("Minesweeper")
            game = Minesweeper(root, width=width, height=height, mines=mines)
            root.mainloop()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid positive integers.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()
