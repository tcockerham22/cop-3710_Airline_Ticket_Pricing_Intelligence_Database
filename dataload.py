import oracledb
import csv
import os 

#Replace with own information
LIB_DIR = r"C:\Users\docto\OneDrive - Florida Polytechnic University\Florida Poly Stuff\Database\InClass\instantclient-basiclite-windows.x64-11.2.0.4.0\instantclient_11_2"
data_dir = r"C:\Users\docto\OneDrive - Florida Polytechnic University\Florida Poly Stuff\Database\Course Project\Part D\data"
DB_USER = "TCOCKERHAM3539_SCHEMA_0ZQNY"
DB_PASS = r"LU4YSUHWRO4IWRDPTMPG0oIHNDYQ$M"
DB_DSN = "db.freesql.com:1521/23ai_34ui2"

oracledb.init_oracle_client(lib_dir=LIB_DIR)

def clear_tables():
    conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
    cursor = conn.cursor()
    tables = ['FareRecord', 'AircraftAssignment', 'AirlineRoute', 'Flight', 'Route', 'Airport', 'Airline']
    for table in tables:
        cursor.execute(f"DELETE FROM {table}")
        print(f"Cleared {table}")
    conn.commit()
    cursor.close()
    conn.close()

def bulk_load_csv(file_path, sql):
    try:
        abs_path = os.path.join(data_dir, file_path)
        print(f"Looking for file at: {abs_path}")

        conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
        cursor = conn.cursor()

        with open(abs_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            data_to_insert = [
                [None if val == '' else val for val in row]
                for row in reader
            ]

        print(f"Starting bulk load of {len(data_to_insert)} rows...")
        cursor.executemany(sql, data_to_insert)
        conn.commit()
        print(f"Successfully loaded {cursor.rowcount} rows into the database.")

    except Exception as e:
        print(f"Error during bulk load: {e}")
        if 'conn' in locals():
            conn.rollback()

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()


clear_tables()
bulk_load_csv('Airline.csv', "INSERT INTO Airline (AirlineID, AirlineName, HeadquartersCountry) VALUES (:1, :2, :3)")
bulk_load_csv('Airport.csv', "INSERT INTO Airport (AirportCode, AirportName, City, AirportState) VALUES (:1, :2, :3, :4)")
bulk_load_csv('Route.csv', "INSERT INTO Route (RouteID, OriginAirport, DestinationAirport, DistanceMiles) VALUES (:1, :2, :3, :4)")
bulk_load_csv('Flight.csv', "INSERT INTO Flight (FlightID, RouteID, FlightNumber, DepartureTime, ArrivalTime) VALUES (:1, :2, :3, TO_TIMESTAMP(:4, 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP(:5, 'YYYY-MM-DD HH24:MI:SS'))")
bulk_load_csv('AirlineRoute.csv', "INSERT INTO AirlineRoute (AirlineID, RouteID, ServiceStartDate, ServiceEndDate) VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), TO_DATE(:4, 'YYYY-MM-DD'))")
bulk_load_csv('AircraftAssignment.csv', "INSERT INTO AircraftAssignment (FlightID, AircraftModel, TailNumber) VALUES (:1, :2, :3)")
bulk_load_csv('FareRecord.csv', "INSERT INTO FareRecord (FlightID, BookingDate, TravelDate, FareAmount) VALUES (:1, TO_DATE(:2, 'YYYY-MM-DD'), TO_DATE(:3, 'YYYY-MM-DD'), :4)")
