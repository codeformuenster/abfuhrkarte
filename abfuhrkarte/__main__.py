from sys import argv

from abfuhrkarte.data import import_calendar, download_csv
from abfuhrkarte.geometry import query_geometries
from abfuhrkarte.html import write_html
from abfuhrkarte.utils import dict_to_jsonfile, dict_from_jsonfile


if __name__ == '__main__':
    if 'load_calendar' in argv:
        csv_data = download_csv()
        calendar = import_calendar(csv_data)

        street_names = list(set([entry.get('strasse') for entry in csv_data]))

        dict_to_jsonfile({
            'street_names': street_names,
            'calendar': calendar,
        }, 'data/calendar.json')
    elif 'build_geometries' in argv:
        data = download_csv()
        street_names = list(set([entry.get('strasse') for entry in data]))
        geometries = query_geometries(street_names)
        dict_to_jsonfile(geometries, 'data/geometries.json')
    elif 'generate_html' in argv:
        geometries = dict_from_jsonfile('data/geometries.json')
        calendar_data = dict_from_jsonfile('data/calendar.json')

        write_html({
            'calendar_data': calendar_data
        })
    else:
        print('wat')
