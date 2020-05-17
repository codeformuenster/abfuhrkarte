import csv
import io
import json
import overpass
import requests
from datetime import datetime

csv_url = 'https://opendata.stadt-muenster.de/sites/default/files/awm_abfuhrdaten_20200512_104053.csv'

overpass_api = overpass.API()


def dict_to_jsonfile(data_dict, path_with_filename):
    with open(path_with_filename, 'w', encoding='utf-8') as outfile:
        json.dump(data_dict, outfile,
                  ensure_ascii=False, sort_keys=True)


def download_csv():
    r = requests.get(csv_url)
    csvio = io.StringIO(r.text, newline="")
    rows = []
    for row in csv.DictReader(csvio, delimiter=';'):
        rows.append(row)
    return rows


def import_calendar(rows):
    # {
    #   "YYYY-MM-DD": {
    #     "waste_type_1": ["street_name_1", ...],
    #     "waste_type_n": ["street_name_m", ...]
    #   }
    # }
    dates_streetnames = {}

    for row in rows:
        date = datetime.strptime(row.get('termin', row.get(
            'termin_vom')), "%d.%m.%Y").strftime("%Y-%m-%d")
        waste_type = row.get('muellart')

        if not date in dates_streetnames:
            dates_streetnames[date] = {}
        if not waste_type in dates_streetnames[date]:
            dates_streetnames[date][waste_type] = []
        dates_streetnames[date][waste_type].append(row.get('strasse'))

    return dates_streetnames


def query_geometry(street_name):
    r = overpass_api.get(
        f'area(3600062591);(way(area)["name"~"{street_name}"]["highway"];);(._;>;)', verbosity='geom')
    # extract the LineString(s)
    features = []
    for f in r.features:
        if f.geometry['type'] == "LineString" and f.properties['highway'] != 'unclassified':
            features.append(f)

    if len(features) == 1:
        return features[0]
    elif len(features) > 1:
        print(
            f'"{street_name}" is built from {len(features)} features. Creating MultiLineSting')
        new_geom = []
        for f in features:
            new_geom.append(f.geometry['coordinates'])

        features[0].geometry['type'] = 'MultiLineString'
        features[0].geometry['coordinates'] = new_geom
        return features[0]


def execute():
    data = download_csv()
    waste_calendar = import_calendar(data)
    dict_to_jsonfile(waste_calendar, 'data/waste_calendar.json')

    geometries = {}
    for entry in data:
        street_name = entry.get('strasse')
        if street_name not in geometries:
            geom = query_geometry(street_name)
            if geom is None:
                print(f'No result for {street_name}')
            geometries[street_name] = geom
            print(".", end='', flush=True)
    dict_to_jsonfile(geometries, 'data/geometries.json')

execute()
