from contextlib import contextmanager
from datetime import datetime
from json import dumps
from locale import LC_ALL, setlocale
from os import makedirs
from shutil import copyfile

from jinja2 import Environment, FileSystemLoader, select_autoescape
from slugify import slugify

from abfuhrkarte.utils import dict_to_jsonfile

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html']),
)


@contextmanager
def locale_de():
    saved = setlocale(LC_ALL)
    try:
        yield setlocale(LC_ALL, 'de_DE.UTF-8')
    finally:
        setlocale(LC_ALL, saved)


def dateformat(value, format='%A, %d.%m.%Y'):
    with locale_de():
        return datetime.strptime(value, "%Y-%m-%d").strftime(format)


def to_title(value, prefix):
    return f'{prefix} {value}'.strip()


def to_json(value):
    return dumps(value)


env.filters['dateformat'] = dateformat
env.filters['to_title'] = to_title
env.filters['to_json'] = to_json
env.filters['slugify'] = slugify


def template_template(template_name, output_filename, data):
    template = env.get_template(template_name)

    with open(output_filename, 'w') as f:
        template.stream(data).dump(f)


def write_html(data):

    makedirs('dist/data', exist_ok=True)

    dates = [date for date in data['calendar_data']]

    waste_types = []
    months = {}
    for date in dates:
        month = date[0:7]
        if month not in months:
            months[month] = []
        months[month].append(date)
        for item in data['calendar_data'][date]:
            waste_types.append(item['waste_type'])

    waste_types = list(set(waste_types))

    geometries_dict = {}
    geometries_slim = {}
    street_names = list(data['geometries'].keys())
    for index in range(len(street_names)):
        new_key = f'{index:x}'
        if data['geometries'][street_names[index]]:
            geometries_slim[new_key] = data['geometries'][street_names[index]]['geometry']
        geometries_dict[street_names[index]] = new_key

    # dict_to_jsonfile(geometries_slim, 'dist/geometries.json')

    template_template('index.j2', 'dist/index.html', {
        'title': '',
        'dates': dates,
        'months': months,
        'scripts': ['hide-past.js'],
    })

    for date in dates:
        makedirs(f'dist/{date}', exist_ok=True)

        date_data = {}
        json_data = {}
        for item in data['calendar_data'][date]:
            district = item['district']
            waste_type = item['waste_type']
            if waste_type not in date_data:
                date_data[waste_type] = {}
            if district not in date_data[waste_type]:
                date_data[waste_type][district] = []

            date_data[waste_type][district].append(item)

            slim_name = geometries_dict[item['street_name']]
            if slim_name not in json_data:
                json_data[slim_name] = {'g': geometries_slim.get(slim_name, None), 'w': []}
            json_data[slim_name]['w'].append(waste_type[:1])


        template_template('date.j2', f'dist/{date}/index.html', {
            'title': dateformat(date),
            'data': date_data,
            'scripts': [],
        })

        dict_to_jsonfile(json_data, f'dist/data/{date}.json')

    makedirs('dist/karte', exist_ok=True)
    template_template('map.j2', 'dist/karte/index.html', {
        'include_leaflet': True,
        'dates': dates,
        'waste_types': waste_types,
        'scripts': ['hide-past.js', 'map.js'],
    })

    for filename in ['hide-past.js', 'map.js', 'abfuhrkarte.css', 'favicon.svg']:
        copyfile(f'templates/{filename}', f'dist/{filename}')
