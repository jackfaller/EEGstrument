#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 10:58:23 2024

@author: jackfaller
"""

import time
import random

# Define the mapping from keys to their letters or chords
key_to_letters = {
    "C": ["C", "D", "E", "F", "G", "A", "B", "C8"],
    "D": ["D", "E", "F#", "G", "A", "B", "C#", "D8"],
    "G": ["G", "A", "B", "C", "D", "E", "F#", "G8"],
    "A": ["A", "B", "C#", "D", "E", "F#", "G#", "A8"],
    "Chords": ["C", "G", "Am", "F"]
}

# Ask the user to input the key
user_key = input("Enter the key (C, D, G, A, or Chords): ")

if user_key not in key_to_letters:
    print("Invalid key entered.")
else:
    start_time = time.time()  # Record the start time
    duration = 300  # Total duration in seconds
    interval = 9.5  # Time between number generations in seconds

    while True:
        current_time = time.time()  # Get the current time
        if current_time - start_time > duration:
            break  # Stop the loop if the total duration has passed

        number = random.randint(1, 8)  # Generate a random number between 1 and 8
        if user_key != "Chords":
            if number <= len(key_to_letters[user_key]):
                print(key_to_letters[user_key][number - 1])  # Print the corresponding note or chord
        else:
            # For chords, since there are 4 chords, we map the numbers to repeat each chord twice
            chord_index = (number - 1) % len(key_to_letters["Chords"])
            print(key_to_letters["Chords"][chord_index])  # Print the corresponding chord

        time.sleep(interval)  # Wait for 9.5 seconds before generating the next number
