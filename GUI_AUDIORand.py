#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 14:35:15 2024

@author: jackfaller
"""
#%% Audio and Function Definitions
import tkinter as tk
from tkinter import ttk  # For the ComboBox
import random
import threading
import pyaudio
import wave


# dictionary of audio files corresponding to each box
audio_files = {
    "C7": r"Notes/notes_A.wav",
    "B": r"Notes/notes_B.wav",
    "A": r"Notes/notes_C.wav",
    "D": r"Notes/notes_D.wav",
    "E": r"Notes/notes_E.wav",
    "F": r"Notes/notes_F.wav",
    "G": r"Notes/notes_G.wav",
    "C8": r"Notes/notes_Gs.wav"
}


audio_files_by_key = {
    "C": {
        "C": r"Notes/notes_A.wav",
        "B": r"Notes/notes_B.wav",
        "A": r"Notes/notes_C.wav",
        "D": r"Notes/notes_D.wav",
        "E": r"Notes/notes_E.wav",
        "F": r"Notes/notes_F.wav",
        "G": r"Notes/notes_G.wav",
        "C8": r"Notes/notes_Gs.wav"
    },
    "D": {
        "D": r"Notes/notes_A.wav",
        "E": r"Notes/notes_B.wav",
        "F#": r"Notes/notes_C.wav",
        "G": r"Notes/notes_D.wav",
        "A": r"Notes/notes_E.wav",
        "B": r"Notes/notes_F.wav",
        "C#": r"Notes/notes_G.wav",
        "D8": r"Notes/notes_Gs.wav"
    },
    "G": {
        "G": r"Notes/notes_A.wav",
        "A": r"Notes/notes_B.wav",
        "B": r"Notes/notes_C.wav",
        "C": r"Notes/notes_D.wav",
        "D": r"Notes/notes_E.wav",
        "E": r"Notes/notes_F.wav",
        "F#": r"Notes/notes_G.wav",
        "G8": r"Notes/notes_Gs.wav"
    },
    "A": {
        "A": r"Notes/notes_A.wav",
        "B": r"Notes/notes_B.wav",
        "C#": r"Notes/notes_C.wav",
        "D": r"Notes/notes_D.wav",
        "E": r"Notes/notes_E.wav",
        "F#": r"Notes/notes_F.wav",
        "G#": r"Notes/notes_G.wav",
        "A8": r"Notes/notes_Gs.wav"
    },
    "Chords": {
        "C": r"Notes/CChord.wav",
        "G": r"Notes/GChord.wav",
        "Am": r"Notes/AmChord.wav",
        "F": r"Notes/FChord.wav",
        "E": r"Notes/notes_E.wav",
        "F#": r"Notes/notes_F.wav",
        "G#": r"Notes/notes_G.wav",
        "A8": r"Notes/notes_Gs.wav"
    }
}



stop_thread = False

# Global variable to manage audio playback thread
audio_thread = None

def play_audio(file_path):
    global audio_thread

    # Define a function to handle audio playback
    def play_thread(path):
        # Open the WAV file
        wf = wave.open(path)

        # Create a PyAudio instance
        p = pyaudio.PyAudio()

        # Open a stream
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # Read data in chunks
        data = wf.readframes(1024)

        # Play stream (3)
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(1024)

        # Stop stream
        stream.stop_stream()
        stream.close()

        # Close PyAudio
        p.terminate()

    # Stop any currently playing audio
    stop_audio()
    play_thread(file_path)
    # Start a new thread for playback
    #audio_thread = threading.Thread(target=play_thread, args=(file_path,))
    #audio_thread.start()

def stop_audio():
    global audio_thread
    # If there's an audio thread running, wait for it to finish
    if audio_thread is not None:
        audio_thread.join()
    # Reset the thread variable
    audio_thread = None


def generate_letter():
    global root, selected_key
    note = random.randint(0, 7)
    print('Note generated', note)
    if selected_key == 'Chords':
        if note == 2 or note == 3:
            note = 1
        elif note == 4 or note == 5 or note == 6:
            note = 2
        elif note == 7:
            note = 3
    print('Note generated', note)
    if all(position == 'normal' for position in box_positions.values()):
        letters = list(boxes.keys())
        selected_letter = letters[note]
        raise_box(selected_letter)
    root.after(2000, generate_letter)


def raise_box(letter):
    global current_highlighted, selected_key
    
    # Reset all boxes to their original state
    for box in boxes.values():
        box.config(highlightbackground="white", highlightthickness=1)
        box.grid_configure(pady=0)  # Reset any padding changes
    
    # Highlight the selected box
    selected_box = boxes[letter]
    selected_box.config(highlightbackground="black", highlightthickness=10)
    current_highlighted = letter

def move_box(selected_key):
    global current_speaker
    global current_highlighted
    if current_highlighted:
        # Reset padding for all boxes
        for letter, box in boxes.items():
            box.grid_configure(pady=(0, 20))

        # Adjust padding for the highlighted box
        box = boxes[current_highlighted]
        if box_positions[current_highlighted] == 'normal':
            box.grid_configure(pady=(20, 0))  # Move the highlighted box up
            box_positions[current_highlighted] = 'raised'
            audio_path = audio_files_by_key[selected_key][current_highlighted]
            threading.Thread(target=play_audio, args=(audio_path,)).start()
        else:
            box.grid_configure(pady=(0, 20))  # Move the highlighted box down
            box_positions[current_highlighted] = 'normal'
            stop_audio()

def exit_application():
    global root
    """Function to exit the application."""
    root.quit()
    root.destroy()  # Close the Tkinter window
    # Optionally, add any clean-up code here
    exit()  # Terminate the Python program






def start_bci_and_calibration():
    global root, start_button, selected_key
    """Function to start BCI and calibration and disable the start button."""
    # Disable the start button to prevent further clicks
    # start_button.config(state=tk.DISABLED)
    root.unbind('c')
    # Start the BCI and calibration in a new thread
    generate_letter()
    # threading.Thread(target=run_bci, daemon=True).start()



#%% CLAUDE 3

# Box dimensions
width = 150
height = 100

colors = ["red", "orange","green", "SeaGreen3", "cyan", "blue",  "purple", "pink"]
# Dictionary mapping musical keys to arrays of letters
key_to_letters = {
    "C": ["C", "D", "E", "F", "G", "A", "B", "C8"],
    "D": ["D", "E", "F#", "G", "A", "B", "C#", "D8"],
    "G": ["G", "A", "B", "C", "D", "E", "F#", "G8"],
    "A": ["A", "B", "C#", "D", "E", "F#", "G#", "A8"],
    "Chords": ["C", "G", "Am", "F"]
}

def main_app(selected_key):
    global root, boxes, box_positions, start_button
    root = tk.Tk()
    root.title("EEGstrument")
    
    # Default letters array if the selected key is not found
    default_letters = ["A7", "B", "C", "D", "E", "F", "G", "A8"]
    letters = key_to_letters.get(selected_key, default_letters)
    
    # Create and place the colored boxes with labels
    boxes = {}
    box_positions = {}  # Track the position of each box
    
    # Adjust window size
    window_width = width * len(letters)
    window_height = height + 150  # Extra space for buttons
    root.geometry(f"{window_width}x{window_height}")
    
    # Informative label at the top of the window
    tk.Label(root, text="For Calibration: Press 'C' then open and close your left hand every second for 20 seconds. \n\nPress Space to Play Selected Note!").grid(row=0, column=0, columnspan=len(colors))
    
    # Create and place colored boxes with labels
    for i, (color, letter) in enumerate(zip(colors, letters)):
        frame = tk.Frame(root, bg=color, width=width, height=height, highlightbackground="white", highlightthickness=1)
        frame.grid(row=1, column=i, pady=(20, 20))  # Adjusted padding for visual separation
        frame.pack_propagate(False)
        label = tk.Label(frame, text=letter, bg=color)
        label.pack(expand=True)  # Fill the frame
        boxes[letter] = frame
        box_positions[letter] = 'normal'
    
    # Create a frame for buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=2, column=0, columnspan=len(colors), pady=30)
    
    # Button configuration within the button_frame using grid
    #move_button = tk.Button(button_frame, text="Move Box", command=move_box)
    #move_button.grid(row=0, column=0, padx=10)
    # Bind the spacebar key to the move_box function
    root.bind('<space>', lambda event: move_box(selected_key))
    root.bind('c', lambda event: start_bci_and_calibration())

    # start_button = tk.Button(button_frame, text="Start Calibration", command=start_bci_and_calibration)
    # start_button.grid(row=0, column=1, padx=10)
    exit_button = tk.Button(button_frame, text="Exit", command=exit_application)
    exit_button.grid(row=0, column=2, padx=10)
    
    # Start the main event loop
    root.mainloop()
#%% SPLASH ROOT


def on_start():
    global selected_key
    selected_key = key_dropdown.get()  # Get the selected musical key from the dropdown
    print(f"Selected Musical Key: {selected_key}")
    
    # Destroy the splash screen
    splash_root.destroy()
    
    # Initialize the main application window
    main_app(selected_key)

# Create the splash screen window
splash_root = tk.Tk()
splash_root.title("Splash Screen")
splash_root.geometry("300x150")

musical_keys = ["C", "D", "G", "A", "Chords"]
key_dropdown = ttk.Combobox(splash_root, values=musical_keys, state="readonly")
key_dropdown.pack(pady=10)
key_dropdown.set("Choose a Key")  # Default/placeholder text

# Add a 'Start' button to the splash screen
start_button_splash = tk.Button(splash_root, text="Start", command=on_start)
start_button_splash.pack(pady=20)

splash_root.mainloop()

# %%
