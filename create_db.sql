CREATE TABLE Airline (
    AirlineID           VARCHAR2(10) PRIMARY KEY,
    AirlineName         VARCHAR2(100) NOT NULL,
    HeadquartersCountry VARCHAR2(100) NOT NULL
);

CREATE TABLE Airport (
    AirportCode     VARCHAR2(10) PRIMARY KEY,
    AirportName     VARCHAR2(100) NOT NULL,
    City            VARCHAR2(100) NOT NULL,
    AirportState    VARCHAR2(100)
);

CREATE TABLE Route (
    RouteID             VARCHAR2(10) PRIMARY KEY,
    OriginAirport       VARCHAR2(10) NOT NULL,
    DestinationAirport  VARCHAR2(10) NOT NULL,
    DistanceMiles       NUMBER       NOT NULL,
    CONSTRAINT fk_origin      FOREIGN KEY (OriginAirport)      REFERENCES Airport(AirportCode),
    CONSTRAINT fk_destination FOREIGN KEY (DestinationAirport) REFERENCES Airport(AirportCode)
);

CREATE TABLE Flight (
    FlightID        VARCHAR2(10) PRIMARY KEY,
    RouteID         VARCHAR2(10) NOT NULL,
    FlightNumber    VARCHAR2(10) NOT NULL,
    DepartureTime   TIMESTAMP    NOT NULL,
    ArrivalTime     TIMESTAMP    NOT NULL,
    CONSTRAINT fk_flight_route FOREIGN KEY (RouteID) REFERENCES Route(RouteID)
);

CREATE TABLE AirlineRoute(
    AirlineID           VARCHAR2(10) NOT NULL,
    RouteID             VARCHAR2(10) NOT NULL,
    ServiceStartDate    DATE         NOT NULL,
    ServiceEndDate      DATE,
    CONSTRAINT pk_airlineroute PRIMARY KEY (AirlineID, RouteID),
    CONSTRAINT fk_airline FOREIGN KEY (AirlineID) REFERENCES Airline(AirlineID),
    CONSTRAINT fk_route FOREIGN KEY (RouteID) REFERENCES Route(RouteID)
);

CREATE TABLE AircraftAssignment (
    FlightID        VARCHAR2(10)  PRIMARY KEY,
    AircraftModel   VARCHAR2(100) NOT NULL,
    TailNumber      VARCHAR2(10)  NOT NULL,
    CONSTRAINT fk_flightid FOREIGN KEY (FlightID) REFERENCES Flight(FlightID)
);

CREATE TABLE FareRecord (
    FlightID    VARCHAR2(10) NOT NULL,
    BookingDate DATE         NOT NULL,
    TravelDate  DATE         NOT NULL,
    FareAmount  NUMBER       NOT NULL,
    CONSTRAINT fk_flight FOREIGN KEY (FlightID) REFERENCES Flight(FlightID),
    CONSTRAINT pk_fare PRIMARY KEY (FlightID, BookingDate, TravelDate)
);