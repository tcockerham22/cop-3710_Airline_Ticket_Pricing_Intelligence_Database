import streamlit as st
import oracledb
import pandas as pd
# --- REQUIRED FOR THICK MODE ---
oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_23_0")

# --- DATABASE CONFIG ---
DB_USER = "TCOCKERHAM3539_SCHEMA_0ZQNY"
DB_PASS = r"LU4YSUHWRO4IWRDPTMPG0oIHNDYQ$M"
DB_DSN = "db.freesql.com:1521/23ai_34ui2"


# --- CONNECT FUNCTION ---
def get_connection():
    return oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)

def run_query(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return pd.DataFrame(rows, columns=columns)

@st.cache_data
def load_airports():
    df = run_query("SELECT AirportCode, AirportName FROM Airport ORDER BY AirportCode")
    df["Display"] = df["AIRPORTCODE"] + " - " + df["AIRPORTNAME"]
    return df

st.title("Airline Database System")

airports_df = load_airports()

feature = st.sidebar.selectbox("Select Feature", [
    "Search Flights",
    "View Airlines on Route",
    "Flights by Aircraft",
    "Price History",
    "Routes from Airport"
])

if feature == "Search Flights":
    st.header("Search Flights")

    origin = st.selectbox("Origin Airport", airports_df["Display"])
    destination = st.selectbox("Destination Airport", airports_df["Display"])
    date = st.date_input("Travel Date")

    if st.button("Search"):
        origin_code = origin.split(" - ")[0]
        dest_code = destination.split(" - ")[0]

        query = """
        SELECT f.FlightID, f.FlightNumber,
               f.DepartureTime, f.ArrivalTime,
               fr.FareAmount
        FROM Flight f
        JOIN Route r ON f.RouteID = r.RouteID
        JOIN FareRecord fr ON f.FlightID = fr.FlightID
        WHERE r.OriginAirport = :origin
          AND r.DestinationAirport = :destination
          AND fr.TravelDate = :travel_date
        """

        df = run_query(query, {
            "origin": origin_code,
            "destination": dest_code,
            "travel_date": date
        })

        st.dataframe(df)

elif feature == "View Airlines on Route":
    st.header("Airlines on Route")

    origin = st.selectbox("Origin Airport", airports_df["Display"], key="air1")
    destination = st.selectbox("Destination Airport", airports_df["Display"], key="air2")

    if st.button("Show Airlines"):
        origin_code = origin.split(" - ")[0]
        dest_code = destination.split(" - ")[0]

        query = """
        SELECT DISTINCT a.AirlineName
        FROM Airline a
        JOIN AirlineRoute ar ON a.AirlineID = ar.AirlineID
        JOIN Route r ON ar.RouteID = r.RouteID
        WHERE r.OriginAirport = :origin
          AND r.DestinationAirport = :destination
        """

        df = run_query(query, {"origin": origin_code, "destination": dest_code})
        st.dataframe(df)

elif feature == "Flights by Aircraft":
    st.header("Flights by Aircraft Model")

    model = st.text_input("Enter Aircraft Model")

    if st.button("Search Aircraft"):
        query = """
        SELECT f.FlightID, f.FlightNumber, aa.AircraftModel
        FROM Flight f
        JOIN AircraftAssignment aa ON f.FlightID = aa.FlightID
        WHERE aa.AircraftModel = :model
        """

        df = run_query(query, {"model": model})
        st.dataframe(df)

elif feature == "Price History":
    st.header("Price History")

    flight_id = st.text_input("Enter Flight ID")

    if st.button("Get Price History"):
        query = """
        SELECT BookingDate, TravelDate, FareAmount
        FROM FareRecord
        WHERE FlightID = :flight_id
        ORDER BY BookingDate
        """

        df = run_query(query, {"flight_id": flight_id})
        st.dataframe(df)

elif feature == "Routes from Airport":
    st.header("Routes from Airport")

    origin = st.selectbox("Origin Airport", airports_df["Display"], key="route")

    if st.button("Show Routes"):
        origin_code = origin.split(" - ")[0]

        query = """
        SELECT DestinationAirport, DistanceMiles
        FROM Route
        WHERE OriginAirport = :origin
        """

        df = run_query(query, {"origin": origin_code})
        st.dataframe(df)