from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html'])
)

def write_html(data):
    # loader = FileSystemLoader('templates')
    # with open('templates/date.j2') as f:
    #     t = jinja2.Template(f.read())
    template = env.get_template('date.j2')
    with open('templates/index.html', 'w') as f:
        f.write(template.render(data))
