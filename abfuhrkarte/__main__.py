from sys import argv

from abfuhrkarte.data import download_and_import, download_csv
from abfuhrkarte.geometry import query_geometries
from abfuhrkarte.utils import dict_to_jsonfile, dict_from_jsonfile


if __name__ == '__main__':
    if 'load_calendar' in argv:
        geoms = dict_from_jsonfile('data/geometries.json')
        print(geoms)
        # calendar = download_and_import()
        # dict_to_jsonfile(calendar, 'data/calendar.json')
    elif 'build_geometries' in argv:
        data = download_csv()
        street_names = list(set([entry.get('strasse') for entry in data]))
        geometries = query_geometries(street_names)
        dict_to_jsonfile(geometries, 'data/geometries.json')
    else:
        print('wat')
