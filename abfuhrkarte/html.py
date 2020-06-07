from contextlib import contextmanager
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from json import dumps
from locale import LC_ALL, setlocale
from os import makedirs
from slugify import slugify
from shutil import copyfile

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

    makedirs('dist', exist_ok=True)
    template_template('index.j2', 'dist/index.html', {
        'title': '',
        'dates': dates,
        'months': months,
        'scripts': ['hide-past.js'],
    })

    for date in dates:
        makedirs(f'dist/{date}', exist_ok=True)

        date_data = {}
        for item in data['calendar_data'][date]:
            district = item['district']
            waste_type = item['waste_type']
            if waste_type not in date_data:
                date_data[waste_type] = {}
            if district not in date_data[waste_type]:
                date_data[waste_type][district] = []

            date_data[waste_type][district].append(item)

        template_template('date.j2', f'dist/{date}/index.html', {
            'title': dateformat(date),
            'data': date_data,
            'scripts': [],
        })

    makedirs('dist/karte', exist_ok=True)
    template_template('map.j2', 'dist/karte/index.html', {
        'include_leaflet': True,
        'dates': dates,
        'waste_types': waste_types,
        'scripts': ['hide-past.js', 'map.js'],
    })



    for filename in ['hide-past.js', 'map.js', 'abfuhrkarte.css', 'favicon.svg']:
        copyfile(f'templates/{filename}', f'dist/{filename}')

    copyfile('data/geometries.json', 'dist/geometries.json')
    copyfile('data/calendar.json', 'dist/calendar.json')
