import csv
import io
import requests

from datetime import datetime

from abfuhrkarte.constants import csv_url


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


def download_and_import():
    return import_calendar(download_csv())
