import tkinter as tk
import random
import threading


# dictionary of audio files corresponding to each box
audio_files = {
    "A7": r"Notes\notes_A.wav",
    "B": r"Notes\notes_B.wav",
    "C": r"Notes\notes_C.wav",
    "D": r"Notes\notes_D.wav",
    "E": r"Notes\notes_E.wav",
    "F": r"Notes\notes_F.wav",
    "G": r"Notes\notes_G.wav",
    "A8": r"Notes\notes_Gs.wav"
}
stop_thread = False

def play_audio():
    print('play audio')


def stop_audio():
    print('stop audio')

def generate_letter():
    note = random.randint(0, 7)

    if all(position == 'normal' for position in box_positions.values()):
        letters = list(boxes.keys())
        selected_letter = letters[note]
        raise_box(selected_letter)
    root.after(2000, generate_letter)


'''Defining the tKinter window'''

def raise_box(letter):
    global current_highlighted
    # Reset all boxes to their original state
    for box in boxes.values():
        box.config(highlightbackground="white", highlightthickness=1)
        box.grid_configure(pady=0)  # Reset any padding changes
    
    # Highlight the selected box
    selected_box = boxes[letter]
    selected_box.config(highlightbackground="black", highlightthickness=10)
    current_highlighted = letter

def generate_letter1():
    if all(position == 'normal' for position in box_positions.values()):
        letters = list(boxes.keys())
        selected_letter = random.choice(letters)
        raise_box(selected_letter)
    root.after(2000, generate_letter)

def exit_application():
    root.quit()
    root.destroy()
    exit()

def move_box():
    if current_highlighted:
        # Reset padding for all boxes
        for letter, box in boxes.items():
            box.grid_configure(pady=(0, 20), in_=boxes_frame)

        # Adjust padding for the highlighted box
        box = boxes[current_highlighted]
        if box_positions[current_highlighted] == 'normal':
            box.grid_configure(pady=(20, 0), in_=boxes_frame)  # Move the highlighted box up
            box_positions[current_highlighted] = 'raised'
        else:
            box.grid_configure(pady=(0, 20), in_=boxes_frame)  # Move the highlighted box down
            box_positions[current_highlighted] = 'normal'

def start_bci_and_calibration():
    start_button.config(state=tk.DISABLED)
    # Placeholder for BCI start function
    # threading.Thread(target=run_bci, daemon=True).start()

# Create the main window
root = tk.Tk()
root.title("Random Box Selector")

# Box and window dimensions
width = 100
height = 100
colors = ["red", "orange","green", "SeaGreen3", "cyan", "blue",  "purple", "pink"]
letters = ["A7", "B", "C", "D", "E", "F", "G", "A8"]

boxes = {}
box_positions = {}
current_highlighted = None

# Separate frames for boxes and buttons
button_frame = tk.Frame(root, pady=30)
button_frame.grid(row=0, column=0, columnspan=len(colors))
boxes_frame = tk.Frame(root)
boxes_frame.grid(row=1, column=0, columnspan=len(colors))


# Create and place the colored boxes within boxes_frame
for i, (color, letter) in enumerate(zip(colors, letters)):
    frame = tk.Frame(boxes_frame, bg=color, width=width, height=height, highlightbackground="white", highlightthickness=1)
    # Corrected grid placement: each frame in its own column
    frame.grid(row=0, column=i, pady=(0, 20), padx=(5, 5))  # Add some padding if needed
    frame.pack_propagate(False)
    label = tk.Label(frame, text=letter, bg=color)
    label.pack(expand=True, fill='both')
    boxes[letter] = frame
    box_positions[letter] = 'normal'

# Create buttons within button_frame
move_button = tk.Button(button_frame, text="Move Box", command=move_box)
move_button.pack(side=tk.LEFT, padx=10)

start_button = tk.Button(button_frame, text="Start Calibration", command=start_bci_and_calibration)
start_button.pack(side=tk.LEFT, padx=10)

exit_button = tk.Button(button_frame, text="Exit", command=exit_application)
exit_button.pack(side=tk.LEFT, padx=10)

start_button = tk.Button(button_frame, text="Start", command=generate_letter())
start_button.pack(side=tk.LEFT, padx=10)

# Adjust window size
window_width = width * len(colors)
window_height = height + 300  # Extra space for buttons
root.geometry(f"{window_width}x{window_height}")



root.mainloop()
