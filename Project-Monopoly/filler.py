import uuid
import os
import time


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


time_buffer = [""] * 12
last_clear_time = time.time()

while True:
    # Update UUIDs
    for i in range(12):
        time_buffer[i] = uuid.uuid4().hex[:8]

    # Clear terminal every 2 seconds
    if time.time() - last_clear_time >= 2:
        clear_terminal()
        last_clear_time = time.time()

    # Print current UUIDs
    print("Latest UUIDs:")
    for i in range(12):
        print(time_buffer)

    time.sleep(0.1)  # Normal speed printing
