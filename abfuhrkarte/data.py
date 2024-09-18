import csv
from datetime import datetime


from abfuhrkarte.constants import csv_filename


def format_date(german_date):
    return datetime.strptime(german_date, "%d.%m.%Y").strftime("%Y-%m-%d")


def format_waste_type(waste_type):
    return waste_type.split(" ")[0].strip(" ,")


def download_file():
    rows = []
    with open(csv_filename, 'r') as reader:
        # csvio = io.StringIO(reader, newline="")
        for row in csv.DictReader(reader, delimiter=';'):
            rows.append(row)
    return rows


def import_calendar(rows):
    # {
    #   "YYYY-MM-DD": {
    #     "waste_type_1": ["street_name_1", ...],
    #     "waste_type_n": ["street_name_m", ...]
    #   }
    # }

    # {
    #   "YYYY-MM-DD": [{
    #     "waste_type": "xxx",
    #     "street_name": "xxx",
    #     "district": "xxx",
    #     "is_original_date": False,
    #     "original_date": "YYYY-MM-DD",
    #   }]
    # }
    calendar = {}

    for row in rows:
        date = format_date(row.get('termin'))
        is_original_date = True
        original_date = None
        try:
            original_date = format_date(row.get('termin_vom'))
            is_original_date = False
        except:
            pass

        waste_type = format_waste_type(row.get('muellart'))

        if date not in calendar:
            calendar[date] = []
        calendar[date].append({
            'waste_type': waste_type,
            'street_name': row.get('strasse'),
            'district': row.get('stadtteil'),
            'is_original_date': is_original_date,
            'original_date': original_date
        })

    return calendar


def download_and_import():
    return import_calendar(download_file())
