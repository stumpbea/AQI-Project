# Libraries
import config
import os
import psycopg2
from sqlalchemy import Table, MetaData
from datetime import datetime

os.environ['MPLCONFIGDIR'] = "/home/AQI"

# Settings
import warnings
warnings.filterwarnings("ignore")

def db_connect(dbname):
    # Funktion verbindet die angegebene DB im localhost container
    engine = psycopg2.connect("host=localhost dbname=" + dbname + " user=admin password=secret")
    conn = config.db_login.connect()
    metadata = MetaData()

    if not config.db_login.dialect.has_table(conn, config.db_AQI_history):
        # Tabelle erstellen
        AQI_history_table = Table(
            config.db_AQI_history,
            metadata,
            autoload=False
        )
        AQI_history_table.create(checkfirst=True)
       
         
# Funktion zur Umwandlung des Timestams in ein Datum
def format_timestamp(date_str):
    parts = date_str[:10]
    parts = parts.split('-')
    return f"{parts[2]}.{parts[1]}.{parts[0][-2:]}"

# Funktion zur Umwandlung des Datums
def format_date(date_str):
    parts = date_str.split('-')
    return f"{parts[2]}.{parts[1]}.{parts[0][-2:]}"

# Funktion zur Umwandlung des Formular Datums
def form_format_date(date_str):
    dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
    output_date = dt.strftime("%Y-%m-%d")
    return output_date

