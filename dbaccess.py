import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('rfid_log.db')
c = conn.cursor()

# Function to fetch and print all data from the database
def print_database():
    c.execute("SELECT * FROM rfid_log")
    rows = c.fetchall()
    for row in rows:
        print(row)

if __name__ == '__main__':
    try:
        print("Fetching and printing data from the database:")
        print_database()
    finally:
        conn.close()
