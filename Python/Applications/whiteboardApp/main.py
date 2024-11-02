import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
from PIL import Image, ImageDraw

class Whiteboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Whiteboard")
        
        # Set up default variables
        self.brush_size = 5
        self.brush_color = "black"
        self.eraser_on = False
        
        # Initialize PIL image for saving
        self.image = Image.new("RGB", (800, 600), "white")
        self.draw = ImageDraw.Draw(self.image)
        
        # Create Canvas
        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack(padx=10, pady=10)
        
        # Bind mouse events to the canvas
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonPress-1>", self.start_pos)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        
        # Initialize variables to store mouse positions
        self.last_x, self.last_y = None, None
        
        # Create buttons
        self.create_buttons()
    
    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack()
        
        # Color Button
        color_btn = tk.Button(button_frame, text="Color", command=self.choose_color)
        color_btn.pack(side=tk.LEFT, padx=5)
        
        # Eraser Button
        eraser_btn = tk.Button(button_frame, text="Eraser", command=self.use_eraser)
        eraser_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear Button
        clear_btn = tk.Button(button_frame, text="Clear", command=self.clear_canvas)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Save Button
        save_btn = tk.Button(button_frame, text="Save", command=self.save_drawing)
        save_btn.pack(side=tk.LEFT, padx=5)
    
    def choose_color(self):
        color = colorchooser.askcolor(color=self.brush_color)[1]
        if color:
            self.brush_color = color
            self.eraser_on = False
    
    def use_eraser(self):
        self.eraser_on = True
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw.rectangle([0, 0, 800, 600], fill="white")
    
    def save_drawing(self):
        file = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG files", "*.png"),
                                                       ("All files", "*.*")])
        if file:
            self.image.save(file)
    
    def start_pos(self, event):
        self.last_x, self.last_y = event.x, event.y
    
    def paint(self, event):
        x, y = event.x, event.y
        if self.last_x and self.last_y:
            if self.eraser_on:
                color = "white"
            else:
                color = self.brush_color
            # Draw on the Tkinter canvas
            self.canvas.create_line(self.last_x, self.last_y, x, y,
                                    width=self.brush_size, fill=color,
                                    capstyle=tk.ROUND, smooth=True)
            # Draw on the PIL image
            self.draw.line([self.last_x, self.last_y, x, y],
                           fill=color, width=self.brush_size)
        self.last_x, self.last_y = x, y
    
    def reset(self, event):
        self.last_x, self.last_y = None, None

if __name__ == "__main__":
    root = tk.Tk()
    app = Whiteboard(root)
    root.mainloop()
