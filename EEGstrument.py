#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 15:45:49 2023

@author: jackfaller
"""

# *****NOTE THE NAME MUST CHANGE!*****
#%% IMPORTS

#import UnicornPy
import neurolThesis
from neurolThesis import streams
from neurolThesis.connect_device import get_lsl_EEG_inlets
from neurolThesis.BCI import generic_BCI, automl_BCI
from neurolThesis import BCI_tools
from neurolThesis.models import classification_tools
from sys import exit
from pylsl import StreamInlet, resolve_stream
import numpy as np
import threading
import soundcard as sc
import wave
import time
import tkinter as tk
from tkinter import ttk  # For the ComboBox
import random


#%% AUDIO

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

def play_audio(file_path):
    """Function to play audio from a given file path."""
    global current_speaker
    global stop_thread
    speaker = sc.default_speaker()
    with wave.open(file_path, 'rb') as wf:
        sample_rate = wf.getframerate()
        num_channels = wf.getnchannels()
        duration = wf.getnframes() / sample_rate
        audio_data = wf.readframes(wf.getnframes())
        audio_data = np.frombuffer(audio_data, dtype=np.int16)
        audio_data = audio_data.reshape(-1, num_channels)
    current_speaker = speaker
    #while not stop_thread:
    speaker.play(audio_data/1000, samplerate=sample_rate)
        #time.sleep(1)
    #stop_thread = False

def stop_audio():
    """Function to stop currently playing audio."""
    global current_speaker
    global stop_thread
    #stop_thread = True
    #speaker = sc.default_speaker()
        # Play a short duration of silence
    #silent_audio = np.zeros((44100, 2), dtype=np.float32)  # 1 second of silence
    #speaker.play(silent_audio, samplerate=44100)
    #current_speaker = None

current_speaker = None

#%% CLASSIFIERS

def clf(clf_input, clb_info):
    #print("clf input" , clf_input)
    clf_input = clf_input[0:2,:clb_info.shape[0]]
    clb_info = clb_info[0:1,:clb_info.shape[0]]
    #print('clb_info.shape[0]', clb_info.shape[0])
    #print("clf input" , clf_input)
    #print('clb_info', clb_info)
    
    # Reshaping clb_info to match the shape of clf_input
    clb_info_reshaped = clb_info.reshape(clf_input.shape)

    # Element-wise comparison and summing
    greater_count = np.sum(clf_input > clb_info_reshaped)

    # Dividing the count by two and ensuring the result is between 0 and 7
    result = np.clip(greater_count // 2, 0, 7)

 
    return result


def clf2(clf_input, clb_info):
    #print("clf input" , clf_input)
    clf_input = clf_input[0:2,:clb_info.shape[0]]
    clb_info = clb_info[0:1,:clb_info.shape[0]]
    #print('clb_info.shape[0]', clb_info.shape[0])
    #print("clf input" , clf_input)
    #print('clb_info', clb_info)
    
    # Extracting the 8th elements from clf_input
    clf_8th_elements = clf_input[:, 7]

    # Reshaping clb_info for comparison
    clb_info_reshaped = clb_info.reshape(clf_input.shape)

    # Comparing the 8th elements of clf_input with each element of clb_info
    comparison_results = np.sum(clb_info_reshaped < clf_8th_elements[:, np.newaxis, np.newaxis], axis=(1, 2))

    # Dividing the total count by two and ensuring the result is between 0 and 7
    result = np.clip(np.sum(comparison_results) // 2, 0, 7)


 
    return result

#%% TKINTER GUI FUNCTIONS


def generate_letter(note):
    print(note)
    if all(position == 'normal' for position in box_positions.values()):
        letters = list(boxes.keys())
        selected_letter = letters[note]
        raise_box(selected_letter)
    #root.after(2000, generate_letter)

def generate_letter1():
    if all(position == 'normal' for position in box_positions.values()):
        letters = list(boxes.keys())
        selected_letter = random.choice(letters)
        raise_box(selected_letter)
    root.after(2000, generate_letter)

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

def move_box():
    global current_speaker
    if current_highlighted:
        # Reset padding for all boxes
        for letter, box in boxes.items():
            box.grid_configure(pady=(0, 20))

        # Adjust padding for the highlighted box
        box = boxes[current_highlighted]
        if box_positions[current_highlighted] == 'normal':
            box.grid_configure(pady=(20, 0))  # Move the highlighted box up
            box_positions[current_highlighted] = 'raised'
            audio_path = audio_files[current_highlighted]
            threading.Thread(target=play_audio, args=(audio_path,)).start()
        else:
            box.grid_configure(pady=(0, 20))  # Move the highlighted box down
            box_positions[current_highlighted] = 'normal'
            stop_audio()

def exit_application():
    """Function to exit the application."""
    root.quit()
    root.destroy()  # Close the Tkinter window
    # Optionally, add any clean-up code here
    exit()  # Terminate the Python program




def start_bci_and_calibration():
    """Function to start BCI and calibration and disable the start button."""
    # Disable the start button to prevent further clicks
    start_button.config(state=tk.DISABLED)
    # Start the BCI and calibration in a new thread
    threading.Thread(target=run_bci, daemon=True).start()

#%% GSPLASH ROOT

# Create the splash window

def on_start():
    selected_key = key_dropdown.get()  # Get the selected musical key from the dropdown
    print(f"Selected Musical Key: {selected_key}") 
    # Destroy the splash screen
    splash_root.destroy()
    # Initialize the main application window
    main_app(selected_key)

# Create the main window


# Create the splash screen window
splash_root = tk.Tk()
splash_root.title("Splash Screen")

# Optionally, you can set the size of the splash screen window
splash_root.geometry("300x150")
musical_keys = ["C",  "D",  "G",  "A"]
key_dropdown = ttk.Combobox(splash_root, values=musical_keys, state="readonly")
key_dropdown.pack(pady=10)
key_dropdown.set("Choose a Key")  # Default/placeholder text

# Add a 'Start' button to the splash screen
start_buttonSplash = tk.Button(splash_root, text="Start", command=on_start)
start_buttonSplash.pack(pady=20)



#%% MAIN ROOT

def main_app(selected_key):
    # Default letters array if the selected key is not found
    default_letters = ["A7", "B", "C", "D", "E", "F", "G", "A8"]
    letters = key_to_letters.get(selected_key, default_letters)

    
    for i, (color, letter) in enumerate(zip(colors, letters)):
        frame = tk.Frame(root, bg=color, width=width, height=height, highlightbackground="white", highlightthickness=1)
        frame.grid(row=0, column=i, pady=(0, 20))  # Default padding
        frame.pack_propagate(False)
        label = tk.Label(frame, text=letter, bg=color)
        label.pack(expand=True, fill='both')
        boxes[letter] = frame
        box_positions[letter] = 'normal'
        
    
    # Start the main event loop
    root.mainloop()

root = tk.Tk()
root.title("EEGstrument")
# Add widgets to the main application window
# Box dimensions
width = 100
height = 100

colors = ["red", "orange","green", "SeaGreen3", "cyan", "blue",  "purple", "pink"]
# Dictionary mapping musical keys to arrays of letters
key_to_letters = {
    "C": ["C", "D", "E", "F", "G", "A", "B", "C8"],
    "D": ["D", "E", "F#", "G", "A", "B", "C#", "D8"],
    "G": ["G", "A", "B", "C", "D", "E", "F#", "G8"],
    "A": ["A", "B", "C#", "D", "E", "F#", "G#", "A8"]
}




# Create and place the colored boxes with labels
boxes = {}
box_positions = {}  # Track the position of each box

# Create a frame for buttons
button_frame = tk.Frame(root, pady= 30)
button_frame.grid(row=4, columnspan=8)


# Create the 'Move' button inside the button frame
move_button = tk.Button(button_frame, text="Move Box", command=move_box)
move_button.pack(side=tk.LEFT, padx=10)

# Create buttons for calibration and exit
start_button = tk.Button(button_frame, text="Start Calibration", command=start_bci_and_calibration)
start_button.pack(side=tk.LEFT, padx=10)

exit_button = tk.Button(button_frame, text="Exit", command=exit_application)
exit_button.pack(side=tk.LEFT, padx=10)


current_highlighted = None  # Track the currently highlighted box

    

# Adjust window size
window_width = width * len(colors)
window_height = height + 300  # Extra space for buttons
root.geometry(f"{window_width}x{window_height}")
tk.Label(root, text="This is the main application window.").pack()



#%% COLLECT LSL STREAM

streams1 = resolve_stream("name='Unicorn'")
inlet = StreamInlet(streams1[0])
stream = streams.lsl_stream(inlet, buffer_length=1024)

#%% INITIALIZE BCI



clb = lambda stream:  BCI_tools.band_power_calibrator(stream, ['EEG 1', 'EEG 2', 'EEG 3', 'EEG 4', 
                                                               'EEG 5', 'EEG 6', 'EEG 7', 'EEG 8'], 'unicorn', 
                                                        bands=['alpha_low','alpha_high'],
                                                        percentile=5, recording_length=10, epoch_len=1, inter_window_interval=0.25)


gen_tfrm = lambda buffer, clb_info: BCI_tools.band_power_transformer(buffer, 250, bands=['alpha_low','alpha_high'])
BCI = generic_BCI(clf, transformer=gen_tfrm, action=generate_letter, calibrator=clb)

def run_bci():
    BCI.calibrate(stream)
    BCI.run(stream)


# Create a thread for BCI operations
bci_thread = threading.Thread(target=run_bci, daemon=True)


#%% RUN THE PROGRAM

# Start the event loop for the splash screen
splash_root.mainloop()
