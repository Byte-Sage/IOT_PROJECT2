import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from gpiozero import Button
import sqlite3
import threading
import time

# Disable GPIO warnings
GPIO.setwarnings(False)

# Initialize the RFID reader
reader = SimpleMFRC522()

# Create Button object for GPIO pin 17
button = Button(17)

# Variable to store RFID tag ID
authorized_id = 497928637258  # Replace with the ID of your authorized RFID tag

# Connect to SQLite database
conn = sqlite3.connect('rfid_log.db')
c = conn.cursor()

# Create RFID log table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS rfid_log (
             timestamp INTEGER,
             id TEXT,
             text TEXT,
             access_status TEXT,
             button_pressed TEXT
             )''')
conn.commit()

# Function to handle button presses
def button_pressed(button_type):
    current_time = int(time.time())
    c.execute("INSERT INTO rfid_log (timestamp, id, text, access_status, button_pressed) VALUES (?, ?, ?, ?, ?)",
              (current_time, authorized_id, "Button press", "Access granted", button_type))
    conn.commit()
    print(f"{button_type} issue registered, RFID ID: {authorized_id}")

# Register the button press event handler
button.when_pressed = button_pressed("Water")  # You can change the button type as needed

# Function to authenticate RFID tag
def authenticate_rfid():
    print("Hold a registered RFID tag near the reader...")
    id, text = reader.read()
    print("ID:", id)
    print("Text:", text)

    # Check if the RFID tag ID is authorized
    if id == authorized_id:
        print("Access granted!")
        current_time = int(time.time())
        c.execute("INSERT INTO rfid_log (timestamp, id, text, access_status) VALUES (?, ?, ?, ?)",
                  (current_time, id, text, "Access granted"))
        conn.commit()
        return True
    else:
        print("Access denied!")
        current_time = int(time.time())
        c.execute("INSERT INTO rfid_log (timestamp, id, text, access_status) VALUES (?, ?, ?, ?)",
                  (current_time, id, text, "Access denied"))
        conn.commit()
        return False

# Function to fetch and print all data from the database
def print_database():
    c.execute("SELECT * FROM rfid_log")
    rows = c.fetchall()
    for row in rows:
        print(row)

if __name__ == '__main__':
    try:
        while True:
            if authenticate_rfid():
                # If RFID authentication is successful, wait for button press for up to 5 seconds
                button.wait_for_press(timeout=5)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        conn.close()
        GPIO.cleanup()
