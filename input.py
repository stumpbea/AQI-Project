
# Imports & Generische Konfig
## Libraries
import config
import requests
import csv
import codecs
import urllib.request
import urllib.error
import sys
import json
import pandas as pd
from bs4 import BeautifulSoup

def model_weather_data(date_str, city):
    BaseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'

    #Key modified to NOT cause accidential costs
    ApiKey='XB2AJ7B74CP7PS8RWU3HY8WME'
    #UnitGroup sets the units of the output - us or metric
    UnitGroup='metric'

    #Location for the weather data
    if city == "Zurich":
        Location='47.39,8.54'
    else:
        Location=city

    #Optional start and end dates
    #If nothing is specified, the forecast is retrieved. 
    #If start date only is specified, a single historical or forecast day will be retrieved
    #If both start and and end date are specified, a date range will be retrieved
    StartDate = date_str
    EndDate= date_str

    #JSON or CSV 
    #JSON format supports daily, hourly, current conditions, weather alerts and events in a single JSON package
    #CSV format requires an 'include' parameter below to indicate which table section is required
    ContentType="csv"

    #include sections
    #values include days,hours,current,alerts
    Include="days"
    #basic query including location
    ApiQuery=BaseURL + Location

    #append the start and end date if present
    if (len(StartDate)):
        ApiQuery+="/"+StartDate
        if (len(EndDate)):
            ApiQuery+="/"+EndDate

    #Url is completed. Now add query parameters (could be passed as GET or POST)
    ApiQuery+="?"

    #append each parameter as necessary
    if (len(UnitGroup)):
        ApiQuery+="&unitGroup="+UnitGroup

    if (len(ContentType)):
        ApiQuery+="&contentType="+ContentType

    if (len(Include)):
        ApiQuery+="&include="+Include

    ApiQuery+="&key="+ApiKey

    print(' - Running query URL: ', ApiQuery)
    print()

    try: 
        CSVBytes = urllib.request.urlopen(ApiQuery)
    except urllib.error.HTTPError  as e:
        ErrorInfo= e.read().decode() 
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()
    except  urllib.error.URLError as e:
        ErrorInfo= e.read().decode() 
        print('Error code: ', e.code,ErrorInfo)
        sys.exit()
        
    # Parse the results as CSV, change lon/lat to string and write to file
    CSVText = csv.reader(codecs.iterdecode(CSVBytes, 'utf-8'))
    
    modified_data = []
    for row in CSVText:
        if row[0] == "47.39,8.54":
            # Ersetzen Sie den Standortwert durch "Zch_Stampfenbachstrasse"
            row[0] = "Zch_Stampfenbachstrasse"
        
        # Fügen Sie die Zeile zur modifizierten Datenliste hinzu
        modified_data.append(row)

    with open(config.csv_temp_weather, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(modified_data)

# Feinstaubdaten für Bestimmten Tag & Statdt auslesen
def AQI_data(date_str, city):

    #Daten der letzten 30 Tage aus Air Quality Index laden
    URL = "https://www.bafu.admin.ch/bafu/de/home/themen/luft/zustand/daten/luftbelastung--historische-daten/nabel--tageswerte-der-letzten-30--tage/werte-der-letzten-30-tage-nabel--feinstaub--pm10-.html"

    f = requests.get(URL)
    soup = BeautifulSoup(f.text)
    
    #slicer - Unnötige Informationen entfernen: Alle Wörter vor dem string "Hoch-geb." werden entfernt sowie alle Wörter nach "Legende". Genau in dieser Spanne sind die eigentlichen Daten.
    strValue = soup.get_text()

    bereinigteListe = strValue.split("Hoch-geb.\n\n\n", 1)
    if len(bereinigteListe) > 0:
        strValue=bereinigteListe[1]

    strValue = strValue.split("\n\n\n\n\n\n\n     Legende", 1)[0]

    #Daten aus Air Quality Index in Tabellen-Format bringen
    data = strValue.split('\n\n')

    data[0] = '\n\n' + data[0]

    columns = data[0].split('\n')[1:]

    rows = [row[1:] for row in data[1:]]

    rows = [row.split('\n') for row in data[1:]]

    rows = [row[:len(columns)] for row in rows]

    AQI_df = pd.DataFrame(rows, columns=columns)

    AQI_df = AQI_df.drop('', axis=1)
    
    AQI_df = AQI_df.iloc[1:]

    PM10 = AQI_df.loc[AQI_df['date'] == date_str, city].values
  
    return PM10
