
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

# Wetterdaten für Bestimmten Tag & Statdt auslesen
def weather_data():

    #Daten aus Open-Meteo (Temperatur, Luftfeuchtigkeit etc.)
    response = requests.get('https://api.open-meteo.com/v1/forecast?latitude=47.37&longitude=8.54&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,precipitation_probability,precipitation,rain,showers,snowfall,snow_depth,weathercode,pressure_msl,surface_pressure,cloudcover,cloudcover_low,cloudcover_mid,cloudcover_high,visibility,evapotranspiration,et0_fao_evapotranspiration,vapor_pressure_deficit,windspeed_10m,windspeed_80m,windspeed_120m,windspeed_180m,winddirection_10m,winddirection_80m,winddirection_120m,winddirection_180m,windgusts_10m,temperature_80m,temperature_120m,temperature_180m,soil_temperature_0cm,soil_temperature_6cm,soil_temperature_18cm,soil_temperature_54cm,soil_moisture_0_1cm,soil_moisture_1_3cm,soil_moisture_3_9cm,soil_moisture_9_27cm,soil_moisture_27_81cm,uv_index,uv_index_clear_sky,is_day,cape,freezinglevel_height,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance,terrestrial_radiation,shortwave_radiation_instant,direct_radiation_instant,diffuse_radiation_instant,direct_normal_irradiance_instant,terrestrial_radiation_instant,temperature_1000hPa,temperature_975hPa,temperature_950hPa,temperature_925hPa,temperature_900hPa,temperature_850hPa,temperature_800hPa,temperature_700hPa,temperature_600hPa,temperature_500hPa,temperature_400hPa,temperature_300hPa,temperature_250hPa,temperature_200hPa,temperature_150hPa,temperature_100hPa,temperature_70hPa,temperature_50hPa,temperature_30hPa,relativehumidity_1000hPa,relativehumidity_975hPa,relativehumidity_950hPa,relativehumidity_925hPa,relativehumidity_900hPa,relativehumidity_850hPa,relativehumidity_800hPa,relativehumidity_700hPa,relativehumidity_600hPa,relativehumidity_500hPa,relativehumidity_400hPa,relativehumidity_300hPa,relativehumidity_250hPa,relativehumidity_200hPa,relativehumidity_150hPa,relativehumidity_100hPa,relativehumidity_70hPa,relativehumidity_50hPa,relativehumidity_30hPa,cloudcover_1000hPa,cloudcover_975hPa,cloudcover_950hPa,cloudcover_925hPa,cloudcover_900hPa,cloudcover_850hPa,cloudcover_800hPa,cloudcover_700hPa,cloudcover_600hPa,cloudcover_500hPa,cloudcover_400hPa,cloudcover_300hPa,cloudcover_250hPa,cloudcover_200hPa,cloudcover_150hPa,cloudcover_100hPa,cloudcover_70hPa,cloudcover_50hPa,cloudcover_30hPa,windspeed_1000hPa,windspeed_975hPa,windspeed_950hPa,windspeed_925hPa,windspeed_900hPa,windspeed_850hPa,windspeed_800hPa,windspeed_700hPa,windspeed_600hPa,windspeed_500hPa,windspeed_400hPa,windspeed_300hPa,windspeed_250hPa,windspeed_200hPa,windspeed_150hPa,windspeed_100hPa,windspeed_70hPa,windspeed_50hPa,windspeed_30hPa,winddirection_1000hPa,winddirection_975hPa,winddirection_950hPa,winddirection_925hPa,winddirection_900hPa,winddirection_850hPa,winddirection_800hPa,winddirection_700hPa,winddirection_600hPa,winddirection_500hPa,winddirection_400hPa,winddirection_300hPa,winddirection_250hPa,winddirection_200hPa,winddirection_150hPa,winddirection_100hPa,winddirection_70hPa,winddirection_50hPa,winddirection_30hPa&models=best_match,ecmwf_ifs04,metno_nordic,gfs_seamless,jma_seamless,icon_seamless,gem_seamless,meteofrance_seamless&daily=weathercode,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,uv_index_max,uv_index_clear_sky_max,precipitation_sum,rain_sum,showers_sum,snowfall_sum,precipitation_hours,precipitation_probability_max,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant,shortwave_radiation_sum,et0_fao_evapotranspiration&past_days=31&timezone=Europe%2FLondon')

    weather_data = json.loads(response.content)
   
    return weather_data

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

    #Daten aus Air Quality Index laden
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
