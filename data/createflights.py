import csv
import random
from datetime import datetime, timedelta

# Generate 1000 records
records = []

for i in range(3001,5000):
    flight_id = i + 2
    flight_number = f"FL{str(flight_id).zfill(3)}"
    departure_date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
    departure_time = (datetime.strptime("08:00:00", "%H:%M:%S") + timedelta(minutes=i)).strftime("%H:%M:%S")
    price = round(random.uniform(1500, 3500), 2)
    destination_base_id = random.randint(1, 12)
    arrival_base_id = random.randint(1, 12)
    arrival_date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
    arrival_time = (datetime.strptime("10:30:00", "%H:%M:%S") + timedelta(minutes=i)).strftime("%H:%M:%S")
    
    record = [flight_id, flight_number, departure_date, departure_time, price, destination_base_id, arrival_base_id, arrival_date, arrival_time]
    records.append(record)

# Write records to CSV file
with open('flights2.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Flight ID", "Flight Number", "Departure Date", "Departure Time", "Price", "Destination Base ID", "Arrival Base ID", "Arrival Date", "Arrival Time"])
    writer.writerows(records)

print("Records generated and saved to flights.csv.")
