import pandas as pd
import os
import re
from datetime import date
import random
import string

#Replace with own information
excel_file_name = r'C:\Users\docto\OneDrive - Florida Polytechnic University\Florida Poly Stuff\Database\Course Project\Course Project data.xlsx'
output_dir = r"C:\Users\docto\OneDrive - Florida Polytechnic University\Florida Poly Stuff\Database\Course Project\Part D\data"

df = pd.read_excel(excel_file_name, sheet_name="Sheet1")

airline_names = df['Airline'].unique()

headquarters = {
    "IndiGo": "India",
    "Air India": "India",
    "Jet Airways": "India",
    "SpiceJet": "India",
    "GoAir": "India",
    "Vistara": "India",
    "Air Asia": "Malaysia",
    "Multiple carriers": "Various",
    "Vistara Premium economy": "India",
    "Jet Airways Business": "India",
    "Multiple carriers Premium economy": "Various",
    "Trujet": "India"
}

aircraftModels = [
    "Airbus A320",
    "Airbus A321",
    "Airbus A319",
    "Boeing 737-800",
    "Boeing 737-900",
    "Boeing 777-300ER",
    "Boeing 787-8",
    "ATR 72-600",
    "Bombardier Q400",
]

airlines = []
for i, name in enumerate(airline_names, start=1):
    airline_id = "A" + str(i)
    country = headquarters.get(name, "Unknown")
    airlines.append([airline_id, name, country])

airline_df = pd.DataFrame(airlines, columns=['AirlineID', 'AirlineName', 'HeadquartersCountry'])
print(airline_df)
print("-------------------------------------------------------")

airport = []
code_to_city = {}

for _, row in df.iterrows():
    if(pd.isna(row['Route'])):
        continue
    codes = row['Route'].split(" → ")
    code_to_city[codes[0]] = row['Source']
    code_to_city[codes[-1]] = row['Destination']

for key, value in code_to_city.items():
    airport.append([key, value + ' Airport', value, None])

airport_df = pd.DataFrame(airport, columns=['AirportCode', 'AirportName', 'City', 'AirportState'])

print(airport_df)
print("-------------------------------------------------------")

route = []
seen_routes = set()
r = 1
for _, row in df.iterrows():
    if(pd.isna(row['Route'])):
        continue
    route_id = "R" + str(r)
    codes = row['Route'].split(" → ")
    originAirport = codes[0]
    destinationAirport = codes[-1]
    duration = row['Duration']
    time = re.findall(r'\d+', duration)
    if(len(time) > 1):
        hours = int(time[0]) + (int(time[1]) /60)
    else:
        hours = int(time[0])
    if (originAirport, destinationAirport) not in seen_routes:
        r += 1
        seen_routes.add((originAirport, destinationAirport))
        route.append([route_id, originAirport, destinationAirport, round((hours * 575), 2)])

route_df = pd.DataFrame(route, columns=['RouteID', 'OriginAirport', 'DestinationAirport', 'Distance'])

print(route_df)
print("-------------------------------------------------------")

flight = []
f = 0
for _, row in df.iterrows():
    if(pd.isna(row['Route'])):
        continue
    f += 1
    flight_id = "F" + str(f)
    flight_num = "FL" + str(f)
    departure = pd.to_datetime(row['Date_of_Journey'] + ' ' + row['Dep_Time'], dayfirst=True)
    duration = row['Duration']
    time = re.findall(r'\d+', duration)
    if len(time) > 1:
        hours = int(time[0]) + (int(time[1]) / 60)
    else:
        hours = int(time[0])
    arrival = departure + pd.Timedelta(hours=hours)
    codes = row['Route'].split(" → ")
    originAirport = codes[0]
    destinationAirport = codes[-1]
    match = route_df[
        (route_df['OriginAirport'] == originAirport) & 
        (route_df['DestinationAirport'] == destinationAirport)
    ]
    route_id = match['RouteID'].values[0]

    flight.append([flight_id, route_id, flight_num, departure, arrival])

flight_df = pd.DataFrame(flight, columns=['FlightID', 'RouteID', 'FlightNumber', 'DepartureTime', 'ArrivalTime'])
flight_df['DepartureTime'] = flight_df['DepartureTime'].dt.strftime('%Y-%m-%d %H:%M:%S')
flight_df['ArrivalTime'] = flight_df['ArrivalTime'].dt.strftime('%Y-%m-%d %H:%M:%S')

print(flight_df)
print("-------------------------------------------------------")

AirlineRoute = []
seen_routes = set()
start = date(2015, 1, 1)
end = date(2019, 1, 1)
for _, row in df.iterrows():
    if(pd.isna(row['Route'])):
        continue
    match_airline = airline_df[airline_df['AirlineName'] == row['Airline']]
    airline_id = match_airline['AirlineID'].values[0]
    codes = row['Route'].split(" → ")
    originAirport = codes[0]
    destinationAirport = codes[-1]
    match = route_df[
        (route_df['OriginAirport'] == originAirport) & 
        (route_df['DestinationAirport'] == destinationAirport)
    ]
    route_id = match['RouteID'].values[0]
    if (airline_id, route_id) not in seen_routes:
        seen_routes.add((airline_id, route_id))
        random_date = start + pd.Timedelta(days=random.randint(0, (end - start).days))
        random_date2 = start + pd.Timedelta(days=random.randint(0, (end - start).days))
        while(random_date2 <= random_date):
            random_date2 = start + pd.Timedelta(days=random.randint(0, (end - start).days))
        end_date = None if random.random() > 0.2 else random_date2
        AirlineRoute.append([airline_id, route_id, random_date, end_date])

AirlineRoute.sort(key=lambda x: int(x[0][1:]))
airlineRoute_df = pd.DataFrame(AirlineRoute, columns=['AirlineID', 'RouteID', 'ServiceStartDate', 'ServiceEndDate'])

print(airlineRoute_df)
print("-------------------------------------------------------")


aircraftAssignment = []
for _, row in flight_df.iterrows():
    flight_id = row['FlightID']
    aircraftModel = random.choice(aircraftModels)
    letters = random.choices(string.ascii_uppercase, k=3)
    tail_number = "VT-" + "".join(letters)
    aircraftAssignment.append([flight_id, aircraftModel, tail_number])

aircraftAssignment_df = pd.DataFrame(aircraftAssignment, columns=['FlightID', 'AircraftModel', 'TailNumber'])

print(aircraftAssignment_df)
print("-------------------------------------------------------")

fareRecord = []
f = 1
for _, row in df.iterrows():
    if(pd.isna(row['Route'])):
        continue
    flight_id = "F" + str(f)
    f += 1
    travel_date = pd.to_datetime(row['Date_of_Journey'], dayfirst=True)
    booking_date = travel_date - pd.Timedelta(days=random.randint(1, 30))
    fareAmount = row['Price']
    fareRecord.append([flight_id, booking_date, travel_date, fareAmount])

fareRecord_df = pd.DataFrame(fareRecord, columns=['FlightID', 'BookingDate', 'TravelDate', 'FareAmount'])

print(fareRecord_df)
print("-------------------------------------------------------")



airline_df.to_csv(f"{output_dir}/Airline.csv", index=False)
airport_df.to_csv(f"{output_dir}/Airport.csv", index=False)
route_df.to_csv(f"{output_dir}/Route.csv", index=False)
flight_df.to_csv(f"{output_dir}/Flight.csv", index=False)
airlineRoute_df.to_csv(f"{output_dir}/AirlineRoute.csv", index=False)
aircraftAssignment_df.to_csv(f"{output_dir}/AircraftAssignment.csv", index=False)
fareRecord_df.to_csv(f"{output_dir}/FareRecord.csv", index=False)