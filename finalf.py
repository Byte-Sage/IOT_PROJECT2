# Function to authenticate RFID tag
def authenticate_rfid():
    print("Hold a registered RFID tag near the reader...")
    id, text = reader.read()
    text = text.strip()  # Trim trailing spaces

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
