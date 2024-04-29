import csv

# Read the CSV file
with open('rfid_button_data.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(reader)

# Remove spaces from each row
for row in data:
    for i, item in enumerate(row):
        row[i] = item.strip()

# Write the modified data back to the CSV file
with open('rfid_button_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("Spaces removed from the CSV file.")

