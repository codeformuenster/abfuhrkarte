import csv
import requests

csv_url = 'https://opendata.stadt-muenster.de/sites/default/files/awm_abfuhrdaten_20200512_104053.csv'

def load_calendar_csv():
    response = requests.get(csv_url)
    reader = csv.reader(response.text, delimiter=' ', quotechar='|')
    for row in reader:
        print(row)

load_calendar_csv()
