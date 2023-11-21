#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 15:45:49 2023

@author: jackfaller
"""

# *****NOTE THE NAME MUST CHANGE!*****

#set git

#import UnicornPy
import neurolThesis
import tkinter as tk

import random

def raise_box(letter):
    global current_highlighted
    # Reset all boxes to their original state
    for box in boxes.values():
        box.config(highlightbackground="white", highlightthickness=1)
        box.grid_configure(pady=0)  # Reset any padding changes
    
    # Highlight the selected box
    selected_box = boxes[letter]
    selected_box.config(highlightbackground="black", highlightthickness=3)
    current_highlighted = letter

def generate_letter():
    if all(position == 'normal' for position in box_positions.values()):
        letters = list(boxes.keys())
        selected_letter = random.choice(letters)
        raise_box(selected_letter)
    root.after(2000, generate_letter)

def move_box():
    if current_highlighted:
        # Reset padding for all boxes
        for letter, box in boxes.items():
            box.grid_configure(pady=(0, 20))

        # Adjust padding for the highlighted box
        box = boxes[current_highlighted]
        if box_positions[current_highlighted] == 'normal':
            box.grid_configure(pady=(20, 0))  # Move the highlighted box up
            box_positions[current_highlighted] = 'raised'
        else:
            box.grid_configure(pady=(0, 20))  # Move the highlighted box down
            box_positions[current_highlighted] = 'normal'



# Create the main window
root = tk.Tk()
root.title("Random Box Selector")

# Box dimensions
width = 100
height = 100

colors = ["red", "green", "blue", "black", "orange", "purple", "pink", "cyan"]
letters = ["A", "B", "C", "D", "E", "F", "G", "H"]

# Create and place the colored boxes with labels
boxes = {}
box_positions = {}  # Track the position of each box

# Create a frame for buttons
button_frame = tk.Frame(root)
button_frame.grid(row=1, columnspan=8)


# Create the 'Move' button inside the button frame
move_button = tk.Button(button_frame, text="Move Box", command=move_box)
move_button.pack(side=tk.LEFT, padx=10)




current_highlighted = None  # Track the currently highlighted box
for i, (color, letter) in enumerate(zip(colors, letters)):
    frame = tk.Frame(root, bg=color, width=width, height=height, highlightbackground="white", highlightthickness=1)
    frame.grid(row=0, column=i, pady=(0, 20))  # Default padding
    frame.pack_propagate(False)
    label = tk.Label(frame, text=letter, bg=color)
    label.pack(expand=True, fill='both')
    boxes[letter] = frame
    box_positions[letter] = 'normal'
    



# Adjust window size
window_width = width * len(colors)
window_height = height + 100  # Extra space for buttons
root.geometry(f"{window_width}x{window_height}")

# Initialize the first call to start the process
generate_letter()

root.mainloop()


#git test