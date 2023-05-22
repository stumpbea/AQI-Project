from sqlalchemy import create_engine
from datetime import datetime, timedelta

##Definition aller Variablen

# File Zeug
## CSV-Dateien mit den Daten
csv_weatherhistory = 'csv-files/Weather_history.csv'
csv_temp_weather = 'csv-files/Temp_weather.csv'

# DB Zeug
## Name der DB
db_name = 'postgres'

## Name der tables
db_weather_history = 'weather_history_table'
db_AQI_history = 'aqi_history_table'

## DB Reference
db_login = create_engine('postgresql://admin:secret@localhost:5432/postgres')

# Datum variablen
## Datum von heute vor 30 Tagen
thirty_days_ago = datetime.today() - timedelta(days=30)
date_heute = datetime.today().strftime("%Y-%m-%d")
date_Vor30Tagen = thirty_days_ago.strftime('%Y-%m-%d')
date_PM10Start = '2023-01-01'
