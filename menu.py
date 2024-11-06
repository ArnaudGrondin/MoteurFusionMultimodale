import tkinter as tk
import subprocess
import sys
import os

def run_script(script_name):
    try:
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running {script_name}: {e}")
    except FileNotFoundError:
        print(f"Error: {script_name} not found in the current directory.")

def train():
    run_script("learner.py")

def recognize():
    run_script("tkDollarN.py")

# Create the main window
root = tk.Tk()
root.title("Gesture Recognition Menu")

# Set window size and position
window_width = 300
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create and pack the Train button
train_button = tk.Button(root, text="Train", command=train, width=20, height=2)
train_button.pack(pady=(20, 10))

# Create and pack the Recognize button
recognize_button = tk.Button(root, text="Recognize", command=recognize, width=20, height=2)
recognize_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()