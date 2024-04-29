import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from gpiozero import Button
from RPLCD.i2c import CharLCD
from time import sleep
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

# Function to handle button presses
def water_fault_button():
    print("Water issue registered")
    lcd.clear()
    lcd.write_string("Water Issue")

def electricity_issue_button():
    print("Electricity issue registered")
    lcd.clear()
    lcd.write_string("Electric Issue")

def wifi_issue_button():
    print("WiFi issue registered")
    lcd.clear()
    lcd.write_string("WiFi Issue")

def projector_issue_button():
    print("Projector issue registered")
    lcd.clear()
    lcd.write_string("Projector Issue")

# Function to authenticate RFID tag
def authenticate_rfid():
    print("Hold a registered RFID tag near the reader...")
    id, text = reader.read()
    print("ID:", id)
    print("Text:", text)

    # Check if the RFID tag ID is authorized
    if id == authorized_id:
        print("Access granted!")
        lcd.clear()
        lcd.write_string("Access granted!")
        return True
    else:
        print("Access denied!")
        lcd.clear()
        lcd.write_string("Access Denied!")
        return False

if __name__ == '__main__':
    try:
        while True:
            if authenticate_rfid():
                # If RFID authentication is successful, wait for button press
                button_water.when_pressed = water_fault_button
                button_electricity.when_pressed = electricity_issue_button
                button_wifi.when_pressed = wifi_issue_button
                button_projector.when_pressed = projector_issue_button
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()
