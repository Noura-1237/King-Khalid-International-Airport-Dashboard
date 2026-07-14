# King-Khalid-International-Airport-Dashboard

# Overview


A comprehensive dataset and interactive dashboard analyzing 153,308 flight records (arrivals and departures) 
at King Khalid International Airport (RUH) 
to explore air traffic patterns, operational efficiency, and scheduling trends.




# Dataset
Dataset Name:King Khalid International Airport Flights Dataset
Source: Kaggle and collected from multiple aviation and flight-tracking APIs

## Dataset Features

The cleaned dataset contains 18 refined columns used for analysis and visualization:

* Flight & Airline Information:
  * Flight_number - The unique identifier for each flight.
  * airline_name - The full name of the operating airline.
  * airline_iata / airline_icao - Standard international airline codes.
  * callSign - The flight's radio call sign.

* Aircraft Details:
  * aircraft_model - The specific model of the aircraft (e.g., Airbus A320, Boeing 777).
  * aircraft_registration - The unique registration number assigned to the aircraft.

* Operational Status & Flight Type:
  * status - Current status of the flight (e.g., Scheduled, Landed, Delayed).
  * flight_type - Type of flight movement (Arrival or Departure).
  * isCargo - Indicator of whether the flight is a cargo operation.
  * terminal - The assigned airport terminal number.

* Destination Details:
  * destination_airport_name - The full name of the destination airport.
  * destination_airport_iata / destination_airport_icao - International airport codes for the destination.
  * destination_timezone - The timezone of the arrival destination.

* Temporal Features (Time & Date):
  * scheduled_time_utc - The scheduled flight time in Coordinated Universal Time (UTC).
  * scheduled_time_local - The scheduled flight time in local Riyadh time.
  * hour - The specific hour extracted from the flight schedule for hourly traffic trend analysis.
  * 
  * ## Key Findings & Insights

* Operational Patterns: Peak traffic hours and workload are unevenly distributed, with specific terminals bearing a significantly higher volume than others.
* Flight Schedules: A strong correlation exists between flight types and their daily schedules, directly impacting terminal density throughout the 24-hour cycle.
* Airlines & Outliers: A few airlines stood out with exceptionally high cancellation rates, signaling potential operational instability.
* Key Takeaway: The dashboard delivers data-driven insights to help optimize staffing, resource allocation, and terminal gate planning while evaluating airline reliability.

* 
* ## Tech Stack

* Language: Python
* Web Framework: Streamlit
* Data Manipulation: Pandas
* Data Visualization: Matplotlib, Seaborn
* Version Control: GitHub



