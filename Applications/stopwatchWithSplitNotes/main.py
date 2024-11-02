import tkinter as tk
from datetime import datetime, timedelta

class StopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch")

        # Stopwatch variables
        self.start_time = None
        self.elapsed_time = timedelta(0)
        self.running = False
        self.splits = []

        # Display the elapsed time with milliseconds
        self.time_display = tk.Label(root, text="00:00:00.000", font=("Helvetica", 24))
        self.time_display.pack()

        # Create buttons for control
        self.start_button = tk.Button(root, text="Start", command=self.start)
        self.pause_button = tk.Button(root, text="Pause", command=self.pause)
        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        self.split_button = tk.Button(root, text="Split", command=self.split)

        # Layout buttons
        self.start_button.pack(side="left")
        self.pause_button.pack(side="left")
        self.stop_button.pack(side="left")
        self.split_button.pack(side="left")

        # Frame for splits
        self.splits_frame = tk.Frame(root)
        self.splits_frame.pack(fill="both", expand=True)

    def start(self):
        if not self.running:
            self.start_time = datetime.now() - self.elapsed_time
            self.running = True
            self.update()  # Start the time update loop

    def pause(self):
        if self.running:
            self.elapsed_time = datetime.now() - self.start_time
            self.running = False

    def stop(self):
        self.running = False
        self.elapsed_time = timedelta(0)
        self.time_display.config(text="00:00:00.000")
        for widget in self.splits_frame.winfo_children():
            widget.destroy()
        self.splits = []

    def split(self):
        if self.running:
            current_time = datetime.now() - self.start_time
            split_text = f"{current_time.seconds // 3600:02}:{(current_time.seconds // 60) % 60:02}:{current_time.seconds % 60:02}.{current_time.microseconds // 1000:03}"

            # Calculate time since the last split
            if self.splits:
                previous_split_time = self.splits[-1][0]
                delta_time = current_time - previous_split_time
            else:
                delta_time = timedelta(0)  # Initialize with 0 for the first split

            delta_text = f"{delta_time.seconds // 3600:02}:{(delta_time.seconds // 60) % 60:02}:{delta_time.seconds % 60:02}.{delta_time.microseconds // 1000:03}"
            
            # Record the split time for future delta calculations
            self.add_split(split_text, delta_text, current_time)

    def add_split(self, split_text, delta_text, split_time):
        # Create a frame for each split entry
        split_frame = tk.Frame(self.splits_frame)
        split_frame.pack(fill="x", padx=5, pady=2)

        # Split label for total time
        split_label = tk.Label(split_frame, text=split_text, width=15, font=("Helvetica", 14))
        split_label.pack(side="left")

        # Delta label for time since last split
        delta_label = tk.Label(split_frame, text=delta_text, width=15, font=("Helvetica", 14))
        delta_label.pack(side="left")

        # Notes entry box for user input
        notes_entry = tk.Entry(split_frame, width=30)
        notes_entry.pack(side="left", padx=5)

        # Store in splits list, recording the exact time of the split for future delta calculations
        self.splits.append((split_time, notes_entry))

    def update(self):
        if self.running:
            # Calculate the updated elapsed time
            self.elapsed_time = datetime.now() - self.start_time
            hours, remainder = divmod(self.elapsed_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            milliseconds = self.elapsed_time.microseconds // 1000
            time_string = f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"
            self.time_display.config(text=time_string)

            # Schedule the next update after 10 ms for smooth millisecond display
            self.root.after(10, self.update)

# Create the main window and run the app
root = tk.Tk()
app = StopwatchApp(root)
root.mainloop()
