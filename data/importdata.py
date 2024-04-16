import csv
from flight.models import FlightSchedule, PlanetBase
from datetime import datetime
'''
to run this program - 
python manage.py shell
then copy and paste the code in the cmd and press enter
'''
def import_flight_schedule_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Extract data from the CSV row
            id, flight_number, departure_date_str, departure_time_str, price_str, destination_base_id, arrival_base_id, arrival_date_str, arrival_time_str = row
            departure_date = datetime.strptime(departure_date_str, '%Y-%m-%d').date()
            departure_time = datetime.strptime(departure_time_str, '%H:%M:%S').time()
            price = float(price_str)
            arrival_date = datetime.strptime(arrival_date_str, '%Y-%m-%d').date()
            arrival_time = datetime.strptime(arrival_time_str, '%H:%M:%S').time()

            # Create and save FlightSchedule instance
            flight_schedule = FlightSchedule.objects.create(
                id=id,
                flight_number=flight_number,
                departure_date=departure_date,
                departure_time=departure_time,
                price=price,
                destination_base_id=destination_base_id,
                arrival_base_id=arrival_base_id,
                arrival_date=arrival_date,
                arrival_time=arrival_time
            )
            flight_schedule.save()

# Usage:
file_path = 'flights2.csv'
import_flight_schedule_from_csv(file_path)