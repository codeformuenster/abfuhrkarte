from datetime import datetime
from os import makedirs
from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html']),
)


def dateformat(value, format='%d.%m.%Y'):
    return datetime.strptime(value, "%Y-%m-%d").strftime(format)


def to_title(value, prefix):
    return f'{prefix} {value}'.strip()


env.filters['dateformat'] = dateformat
env.filters['to_title'] = to_title


def template_template(template_name, output_filename, data):
    template = env.get_template(template_name)

    with open(output_filename, 'w') as f:
        template.stream(data).dump(f)


def write_html(data):
    makedirs('dist', exist_ok=True)
    template_template('index.j2', 'dist/index.html', {
        **{'title': ''},
        **data
    })

    for date in data['calendar_data']['calendar']:
        makedirs(f'dist/{date}', exist_ok=True)
        template_template('date.j2', f'dist/{date}/index.html', {
            'title': dateformat(date),
            'date_data': data['calendar_data']['calendar'][date],
        })
