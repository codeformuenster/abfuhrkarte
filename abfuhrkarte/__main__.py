from sys import argv

from abfuhrkarte.data import import_calendar, download_csv
from abfuhrkarte.geometry import query_geometries
from abfuhrkarte.utils import dict_to_jsonfile, dict_from_jsonfile
from abfuhrkarte.constants import calendar_filename, geometries_filename


if __name__ == '__main__':
    if 'load_calendar' in argv:
        csv_data = download_csv()
        calendar = import_calendar(csv_data)

        dict_to_jsonfile(calendar, calendar_filename)
    elif 'build_geometries' in argv:
        data = download_csv()
        street_names = list(set([entry.get('strasse') for entry in data]))
        geometries = query_geometries(street_names)
        dict_to_jsonfile(geometries, geometries_filename)
    elif 'generate_html' in argv:
        from abfuhrkarte.html import write_html

        # geometries = dict_from_jsonfile(geometries_filename)
        calendar_data = dict_from_jsonfile(calendar_filename)

        write_html({
            'calendar_data': calendar_data
        })
    else:
        print('command required:')
        print()
        print('load_calendar ->')
        print(f'  download csv calendar and store in {calendar_filename}')
        print()
        print(
            f'build_geometry -> (requires {calendar_filename} generated by load_calendar')
        print(
            f'  query street geometries from overpass and store in {geometries_filename}')
        print('make sure to configure a suitable overpass instance in constants.py')
        print()
        print(
            f'generate_html -> (requires {calendar_filename} generated by load_calendar')
        print('  template html files into dist folder')
        print()
