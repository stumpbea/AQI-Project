# AQI Project

## Variablen
Die wichtigsten globalen Variablen sind im File config.py abgelegt.
Um sie zu verwenden muss das File zu beginn jedes Codes importiert werden => import config
Die Variablen können über config.<Varibale> im Code verwendet werden.

## Preprocessing Funktionen
Die wichtigsten Funktionen sind im File preprocessing_functions.py definiert.
Um sie zu verwenden muss das File zu beginn jedes Codes importiert werden => import preprocessing_functions as pf
Die Funktionen können über pf.<Funktion> im Code verwendet werden.

## Datenbank
Die Datenbank wird als Docker Container instanziiert
Um den container zu instanziieren muss das File docker-compose.yml ausgeführt werden

## Historischer Daten input
Die historischen Wetterdaten seit 2001 werden im File Weatherdata_API.ipynb einmalig von visualcrossing.com runtergeladen und in das CSV-File csv-files/Weather_history.csv geladen.
Dies wird getrennt behandelt, damit der kostenpflichtige Download nicht x-fach ausgeführt wird.
Das effektive Laden der historischen Input Files passiert dann im File input_history.ipynb. 
Dort wird mit einem WebScraper die website der stadt Zürich abgesucht und die CSV-Files zur Luftqualität (1 File pro Jahr) werden heruntergeladen und ebenfalls im folder csv-files abgelegt.
Anschliessend werden die Files iterative geöffnet, gefiltert und die resultierenden Daten in die Datenbank gespeichert.
Auch das csv-file Weather_history.csv wird geöffnet, geringfügig umformatiert und dann in die DB geladen.
Last but not least werden die Daten angereichert und die neuen Felder ebenfalls in der DB hinzugefügt.

## Explorative Datenanalyse
Im File eda.ipynb werden die Daten geladen, gesichtet, analysiert und die am besten geeigneten Attribute ausgewählt

## Modellerstellung
Die erstellung des Models erfolgt über das File model.ipynb
Es erstellt verschiedene Modelle und vergleicht sie anhand von RMSE, MAE, MSE, R2, Explained Variance score 
Als Ergebnis der Modellierung wird das beste Model im File AQI_model.pkl bereitgestellt.

## Presentation
Die Hauptaplikation wird aus dem File presentation.ipynb gestartet
Dort wird mittels flask ein webserver erstellt, der auf die beiden Pages home.html und prediction.html zugreift
Er nutzt das Formular AQI_form.py für die übergabe von Werten.
Die Applikation ruft zudem über das file input.py die aktuellen Daten für den fraglichen Zeitraum und Ort ab.
Anschliessend ruft sie mit den vorbereiteten Daten das Modell AQI_model.pkl auf und gibt das Resultat aus.

