#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 8 15:45:49 2023

@author: jackfaller
"""

import tkinter as tk
import random
import threading
import numpy as np
import soundcard as sc
import wave
from pylsl import StreamInlet, resolve_stream

# Importing custom modules
import neurolThesis
from neurolThesis import streams
from neurolThesis.BCI import generic_BCI
from neurolThesis import BCI_tools

# Global variables for audio playback
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
current_speaker = None
stop_thread = False

# Audio playback functions
def play_audio(file_path):
    """Function to play audio from a given file path."""
    global current_speaker
    speaker = sc.default_speaker()
    with wave.open(file_path, 'rb') as wf:
        sample_rate = wf.getframerate()
        num_channels = wf.getnchannels()
        audio_data = wf.readframes(wf.getnframes())
        audio_data = np.frombuffer(audio_data, dtype=np.int16).reshape(-1, num_channels)
    current_speaker = speaker
    speaker.play(audio_data / 1000, samplerate=sample_rate)

def stop_audio():
    """Function to stop currently playing audio."""
    global current_speaker
    # Placeholder for stopping audio; implement as needed.

# BCI-related functions
def clf(clf_input, clb_info):
    """Example classifier function."""
    # Function body; implement classification logic as needed.
    return 0

def run_bci():
    """Function to run BCI calibration and start BCI stream processing."""
    streams1 = resolve_stream("name='Unicorn'")
    inlet = StreamInlet(streams1[0])
    stream = streams.lsl_stream(inlet, buffer_length=1024)
    clb = lambda stream: BCI_tools.band_power_calibrator(stream, ['EEG 1', 'EEG 2', 'EEG 3', 'EEG 4', 
                                                                   'EEG 5', 'EEG 6', 'EEG 7', 'EEG 8'], 'unicorn', 
                                                          bands=['alpha_low', 'alpha_high'],
                                                          percentile=5, recording_length=5, epoch_len=1, inter_window_interval=0.25)
    gen_tfrm = lambda buffer, clb_info: BCI_tools.band_power_transformer(buffer, 250, bands=['alpha_low', 'alpha_high'])
    BCI = generic_BCI(clf, transformer=gen_tfrm, action=generate_letter, calibrator=clb)
    BCI.calibrate(stream)
    BCI.run(stream)

# Tkinter GUI functions
def raise_box(letter):
    """Highlight a specific box in the GUI."""
    global current_highlighted
    for box in boxes.values():
        box.config(highlightbackground="white", highlightthickness=1)
        box.grid_configure(pady=0)
    selected_box = boxes[letter]
    selected_box.config(highlightbackground="black", highlightthickness=10)
    current_highlighted = letter

def generate_letter(note):
    """Generate a letter and highlight the corresponding box."""
    if all(position == 'normal' for position in box_positions.values()):
        letters = list(boxes.keys())
        selected_letter = letters[note]
        raise_box(selected_letter)

def move_box():
    """Move the highlighted box up or down."""
    global current_speaker
    if current_highlighted:
        for letter, box in boxes.items():
            box.grid_configure(pady=(0, 20))
        box = boxes[current_highlighted]
        if box_positions[current_highlighted] == 'normal':
            box.grid_configure(pady=(20, 0))
            box_positions[current_highlighted] = 'raised'
            audio_path = audio_files[current_highlighted]
            threading.Thread(target=play_audio, args=(audio_path,)).start()
        else:
            box.grid_configure(pady=(0, 20))
            box_positions[current_highlighted] = 'normal'
            stop_audio()

def exit_application():
    """Exit the application."""
    root.quit()
    root.destroy()
    exit()

# Main GUI setup
root = tk.Tk()
root.title("Random Box Selector")
width, height = 100, 100
colors = ["red", "orange", "green", "SeaGreen3", "cyan", "blue", "purple", "pink"]
letters = ["A7", "B", "C", "D", "E", "F", "G", "A8"]
boxes = {}
box_positions = {}
current_highlighted = None

for i, (color, letter) in enumerate(zip(colors, letters)):
    frame = tk.Frame(root, bg=color, width=width, height=height, highlightbackground="white", highlightthickness=1)
    frame.grid(row=0, column=i, pady=(0, 20))
    frame.pack_propagate(False)
    label = tk.Label(frame, text=letter, bg=color)
    label.pack(expand=True, fill='both')
    boxes[letter] = frame
    box_positions[letter] = 'normal'

button_frame = tk.Frame(root, pady=30)
button_frame.grid(row=4, columnspan=8)
move_button = tk.Button(button_frame, text="Move Box", command=move_box)
move_button.pack(side=tk.LEFT, padx=10)
start_button = tk.Button(button_frame, text="Start Calibration", command=lambda: threading.Thread(target=run_bci, daemon=True).start())
start_button.pack(side=tk.LEFT, padx=10)
exit_button = tk.Button(button_frame, text="Exit", command=exit_application)
exit_button.pack(side=tk.LEFT, padx=10)

window_width = width * len(colors)
window_height = height + 300
root.geometry(f"{window_width}x{window_height}")
root.mainloop()
