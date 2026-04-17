import tkinter as tk
from tkinter import ttk, messagebox
import oracledb
from tkcalendar import DateEntry
# --- REQUIRED FOR THICK MODE ---
oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_23_0")

# --- DATABASE CONFIG ---
DB_USER = "TCOCKERHAM3539_SCHEMA_0ZQNY"
DB_PASS = r"LU4YSUHWRO4IWRDPTMPG0oIHNDYQ$M"
DB_DSN = "db.freesql.com:1521/23ai_34ui2"


# --- CONNECT FUNCTION ---
def get_connection():
    return oracledb.connect(
        user=DB_USER,
        password=DB_PASS,
        dsn=DB_DSN
    )


# LOAD AIRPORTS INTO DROPDOWN

def load_airports():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT AirportCode || ' - ' || AirportName
            FROM Airport
            ORDER BY AirportCode
        """)

        airports = [row[0] for row in cursor]

        origin_dropdown['values'] = airports
        dest_dropdown['values'] = airports

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error loading airports", str(e))

# ==============================
# EXTRACT AIRPORT CODE
# ==============================
def extract_code(selection):
    return selection.split(" - ")[0]

# ==============================
# SEARCH FUNCTION (ROUND TRIP)
# ==============================
def search_flights():
    origin_sel = origin_dropdown.get()
    dest_sel = dest_dropdown.get()
    travel_date = depart_date.get()
    return_date_val = return_date.get()

    if not origin_sel or not dest_sel:
        messagebox.showerror("Error", "Select both airports")
        return

    origin = extract_code(origin_sel)
    destination = extract_code(dest_sel)

    if origin == destination:
        messagebox.showerror("Error", "Origin and destination cannot be the same")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Clear table
        for row in tree.get_children():
            tree.delete(row)

        # ==========================
        # OUTBOUND FLIGHTS
        # ==========================
        outbound_query = """
        SELECT 'OUTBOUND',
               f.FlightID,
               f.FlightNumber,
               f.DepartureTime,
               f.ArrivalTime,
               fr.FareAmount
        FROM Flight f
        JOIN Route r ON f.RouteID = r.RouteID
        JOIN FareRecord fr ON f.FlightID = fr.FlightID
        WHERE r.OriginAirport = :origin
          AND r.DestinationAirport = :destination
          AND fr.TravelDate = TO_DATE(:travel_date, 'YYYY-MM-DD')
        """

        cursor.execute(outbound_query,
                       origin=origin,
                       destination=destination,
                       travel_date=travel_date)

        outbound_rows = cursor.fetchall()

        # ==========================
        # RETURN FLIGHTS
        # ==========================
        return_query = """
        SELECT 'RETURN',
               f.FlightID,
               f.FlightNumber,
               f.DepartureTime,
               f.ArrivalTime,
               fr.FareAmount
        FROM Flight f
        JOIN Route r ON f.RouteID = r.RouteID
        JOIN FareRecord fr ON f.FlightID = fr.FlightID
        WHERE r.OriginAirport = :destination
          AND r.DestinationAirport = :origin
          AND fr.TravelDate = TO_DATE(:return_date, 'YYYY-MM-DD')
        """

        cursor.execute(return_query,
                       origin=origin,
                       destination=destination,
                       return_date=return_date_val)

        return_rows = cursor.fetchall()

        all_rows = outbound_rows + return_rows

        if not all_rows:
            messagebox.showinfo("No Results", "No flights found for selected dates")
            return

        # Insert into table
        for row in all_rows:
            tree.insert("", "end", values=row)

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# ==============================
# CLEAR FUNCTION
# ==============================
def clear_results():
    origin_dropdown.set("")
    dest_dropdown.set("")
    for row in tree.get_children():
        tree.delete(row)

# ==============================
# GUI SETUP
# ==============================
root = tk.Tk()
root.title("Flight Search System (Oracle Thick Mode)")
root.geometry("800x500")

# --- ORIGIN ---
tk.Label(root, text="Origin Airport").pack()
origin_dropdown = ttk.Combobox(root, state="readonly", width=40)
origin_dropdown.pack()

# --- DESTINATION ---
tk.Label(root, text="Destination Airport").pack()
dest_dropdown = ttk.Combobox(root, state="readonly", width=40)
dest_dropdown.pack()

# --- DEPART DATE ---
tk.Label(root, text="Departure Date").pack()
depart_date = DateEntry(root, date_pattern='yyyy-mm-dd')
depart_date.pack()

# --- RETURN DATE ---
tk.Label(root, text="Return Date").pack()
return_date = DateEntry(root, date_pattern='yyyy-mm-dd')
return_date.pack()

# --- BUTTONS ---
tk.Button(root, text="Search Flights", command=search_flights).pack(pady=10)
tk.Button(root, text="Clear", command=clear_results).pack()

# ==============================
# RESULTS TABLE
# ==============================
columns = ("TripType", "FlightID", "FlightNumber",
           "DepartureTime", "ArrivalTime", "FareAmount")

tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(expand=True, fill="both")

# ==============================
# LOAD DATA
# ==============================
load_airports()

# ==============================
# RUN APP
# ==============================
root.mainloop()