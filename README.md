# cop-3710_Airline_Ticket_Pricing_Intelligence_Database

Application Domain:
The application domain for this project is airline pricing analytics. This system models airfaire price fluctuations based on trends and seasonality.

Goals:
- Store and manage historical airfare pricing across different locations and dates
- Analyze trends across seasonal pricing patterns
- Provide a structured database for reporting and visualization

Database Overview:
The system includes core entities such as Airline, Airport, Route, and Flight, along with a weak entity to track time-based fare changes and an associative entity to model airline participation on routes. A key design challenge is accurately representing fare fluctuations over time using composite keys while maintaining clear one-to-one, one-to-many, and many-to-many relationships

Data Sources:
- https://www.kaggle.com/datasets/nikhilmittal/flight-fare-prediction-mh
