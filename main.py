# Program to detect mouse movement. Logs mouse position while moving mouse. On left click start recording on new file.
# Stops recording on left click. Records mouse position with time for each movement and sum of all time.

# Important: to use program verson 3.11 python is needed ( pynput module wont work on newer vresions of python)!!!

import pyautogui
import time
from pynput import mouse

# Variable to track last known mouse position and time
last_position = pyautogui.position()
last_time = time.time()
recording = False  # Start with recording off
log_file = None
file_counter = 1

def on_move(x, y):
    global last_position, last_time, recording, log_file
    # Logs current position of the mouse;
    print(f"({x}, {y})")
    if not recording or log_file is None:
        return
    
    # Records time of the movement;
    current_time = time.time()
    duration = current_time - last_time
    
    if (x, y) != last_position:
        with open(log_file, "a") as file:
            file.write(f"Start: {last_position}, End: ({x}, {y}), Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time))}, End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))}, Duration: {duration:.4f} sec\n")
        last_position = (x, y)
        last_time = current_time

# Creating new file and recording positions and time on mouse click event;
def on_click(x, y, button, pressed):
    global recording, log_file, file_counter
    if pressed and button == mouse.Button.left:
        if recording:
            print("Mouse left click detected. Stopping recording.")
            recording = False
            log_file = None
        else:
            log_file = f"mouse_movement_log_{file_counter}.txt"
            file_counter += 1
            print(f"Mouse left click detected. Starting new recording in {log_file}.")
            with open(log_file, "w") as file:
                file.write("New Recording Session:\n")
            recording = True

# Start listening to mouse events
with mouse.Listener(on_move=on_move, on_click=on_click) as listener:
    print("Recording mouse movement. Left click to stop/start a new recording in a new file.")
    listener.join()
