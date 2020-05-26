# Abfuhrkarte Münster

Heavily WIP!

## Quickstart

Requires Python 3.8

- `pip install -r requirements.txt`
- `python -m abfuhrkarte load_calendar`
- `python -m abfuhrkarte generate_html`

## For the future: Geometries

We're using static map data from OpenStreetMap. Usually this does not need to be touched unless you're sure the data needs to be updated.

The already available map is generated using a local overpass instance and `python -m abfuhrkarte build_geometries`.
