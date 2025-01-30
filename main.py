# Program to detect mouse movement. Logs mouse position while moving mouse. On left click start recording on new file.
# Stops recording on left click. Records mouse position with time for each movement and sum of all time.

# Important: to use program verson 3.11 python is needed ( pynput module wont work on newer vresions of python)!!!

import pyautogui
import time
from pynput import mouse
import json

# Variable to track recording state, file, and session data
recording = False  # Start with recording off
log_file = None
file_counter = 1
mouse_positions = []
session_start_time = None

def on_move(x, y):
    global recording, mouse_positions
    print(f"Current Mouse Position: ({x}, {y})")
    if not recording:
        return
    
    mouse_positions.append((x, y))

def on_click(x, y, button, pressed):
    global recording, log_file, file_counter, mouse_positions, session_start_time
    if pressed and button == mouse.Button.left:
        if recording:
            print("Mouse left click detected. Stopping recording.")
            if log_file:
                total_time = round(time.time() - session_start_time, 4)
                session_data = {
                    "movements": mouse_positions,
                    "total_time": total_time
                }
                with open(log_file, "w") as file:
                    json.dump(session_data, file, indent=4)
            recording = False
            log_file = None
            mouse_positions = []
        else:
            log_file = f"mouse_movement_log_{file_counter}.json"
            file_counter += 1
            print(f"Mouse left click detected. Starting new recording in {log_file}.")
            recording = True
            mouse_positions = []
            session_start_time = time.time()

# Start listening to mouse events
with mouse.Listener(on_move=on_move, on_click=on_click) as listener:
    print("Recording mouse movement. Left click to stop/start a new recording in a new file.")
    listener.join()
