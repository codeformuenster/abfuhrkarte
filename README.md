# Abfuhrkarte Münster

Heavily WIP! Visualization of the waste collection in Münster.

Uses the Dataset [Entsorgungskalender 2020 der Abfallwirtschaftsbetriebe Münster (AWM)](https://opendata.stadt-muenster.de/dataset/ entsorgungskalender-2020-der-abfallwirtschaftsbetriebe-m%C3%BCnster-awm).

Currently hosted at [https://abfuhrkarte.codeformuenster.org/](https://abfuhrkarte.codeformuenster.org/).

## Quickstart

Requires Python 3.8

- `pip install -r requirements.txt`
- `python -m abfuhrkarte load_calendar`
- Check [`abfuhrkarte/constants`](abfuhrkarte/constants.py). Change `overpass_endpoint_url` to the Overpass instance you want to use.
- `python -m abfuhrkarte build_geometries`
- `python -m abfuhrkarte generate_html`

You now have the static html in the `dist` directory.

## Geometries

We're using static map data from OpenStreetMap. Usually this does not need to be touched unless you're sure the data needs to be updated.

The already available map is generated using a local overpass instance and `python -m abfuhrkarte build_geometries`.
