import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from gpiozero import Button
from RPLCD.i2c import CharLCD
from datetime import datetime
import csv
# Disable GPIO warnings
GPIO.setwarnings(False)

# Initialize the RFID reader
reader = SimpleMFRC522()
lcd = CharLCD('PCF8574', 0x27)

# Create Button objects for GPIO pins
button_wifi = Button(17)
button_projector = Button(18)
button_electricity = Button(27)
button_water = Button(22)

# Variable to store RFID tag ID
authorized_id = 497928637258  # Replace with the ID of your authorized RFID tag

# Global variables for RFID tag ID and text
idd = None
textt = None

# Function to authenticate RFID tag
def authenticate_rfid():
    global idd, textt  # Declare idd and textt as global variables
    print("Hold a registered RFID tag near the reader...")
    idd, textt = reader.read()
    print("ID:", idd)
    print("Text:", textt)

    # Check if the RFID tag ID is authorized
    if idd == authorized_id:
        print("Access granted!")
        lcd.clear()
        lcd.write_string("Access granted!")
        record_data("Access granted", idd, textt,"")
        return True
    else:
        print("Access denied!")
        lcd.clear()
        lcd.write_string("Access Denied!")
        record_data("Access denied", idd, textt,"")
        return False

# Functions to handle button presses
def water_fault_button():
    print("Water issue registered")
    lcd.clear()
    lcd.write_string("Water Issue")
    record_data("Water Issue", idd, textt,"Not Resolved")

def electricity_issue_button():
    print("Electricity issue registered")
    lcd.clear()
    lcd.write_string("Electric Issue")
    record_data("Electricity Issue", idd, textt,"Not Resolved")

def wifi_issue_button():
    print("WiFi issue registered")
    lcd.clear()
    lcd.write_string("WiFi Issue")
    record_data("WiFi Issue", idd, textt,"Not Resolved")

def projector_issue_button():
    print("Projector issue registered")
    lcd.clear()
    lcd.write_string("Projector Issue")
    record_data("Projector Issue", idd, textt,"Not Resolved")

# Function to record data with timestamp, event, RFID ID, and text
def record_data(event, idd, textt,status):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    with open('rfid_button_data.csv', mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, event, idd, textt,status])

if __name__ == '__main__':
    try:
        while True:
            if authenticate_rfid():
                # If RFID authentication is successful, wait for button press
                button_water.when_released = water_fault_button
                button_electricity.when_released = electricity_issue_button
                button_wifi.when_released = wifi_issue_button
                button_projector.when_released = projector_issue_button
    except KeyboardInterrupt:
        import rmsp
        print("Exiting...")
    finally:
        GPIO.cleanup()

