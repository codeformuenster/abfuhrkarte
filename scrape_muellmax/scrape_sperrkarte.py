import json
import requests
import time
from icalendar import Calendar, Event
from parsel import Selector

base_url = "https://www.muellmax.de/abfallkalender/awm/res/AwmStart.php"
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

# dict:
#   keys: iso8601 dates
#   values: arrays of street names
dates_streetnames = {}


def request_street_names():
    data = {
        'xxx': '1',
        'mm_ses': 'bW5oQmc2RmxuMVo5N1hGbUNlWXcyU3VzNGVVN0QwL3RZVGxIV090TitDcHJacGVIVXdGUlhzbEw5UEVXczhwS3JtSGNZZW1vUjBEbmJGL2l5Tk13Q3M3b01wK09FTzdyakphSlJ4VXg5VEhVTGt5QmVpOUY1QmpJU0lsa01HZmRreW83TGtGa1ZMMVRyaG0zcVBIMzlxelNuSUU1cTJvTFhlckZCcDlRVjdmamZJN2ZNRFlLTmdkOFgwRXBVV1lvd0pVdEtxb1Bkc0hqMy9OQk11aTVKSGprQ3lKazEwZ0VwWlNuMkt0UHhyY3dMNzVnaTVhQ053MVpwOEdZN0txQzRLYVI5aTJrMjFBTWx2SFVQd3hmMnc9PQ==',
        'mm_frm_str_name': '',
        'mm_aus_str_txt_submit': 'suchen',
    }
    response = requests.post(base_url, headers=headers, data=data)
    selector = Selector(text=response.text)

    return selector.css("select#mm_frm_str_sel option::attr(value)").getall()


def create_session(street_name):
    data = {
        'xxx': '1',
        'mm_ses': 'bW5oQmc2RmxuMVo5N1hGbUNlWXcyWE1hWUdmdXBRaSsrMFlvZm1KMS9VQ3h6VXRMRkpLeUhHVFNseXVFZWwzSUhGN2xiaFh2VWM5OHRSbTllV25TVWJScFM3clVScFJwMTVSS1hud3ZBOXY4c0RqeDErTXFpTTBsSGVldDJKZXpSZTdOeU9ENjlLcWlmd3ZwbnVSWlQ5MWx1dzd2d1pjUHlHY1dVVG5uaURCN0F2emUrUU9jQXBkN09vSCtibVI0RlpWUkF5RDFIdGUzcUNKck94OVlKUjBRTnVla05VSlJmSUxMNVJVWTFLTklEVHRlQStEOXRPQ3pscW1PeUFWNTRDQXl3WVRTQmk0TzZ4WFVaOGdqZ1E9PQ==',
        'mm_frm_str_name': street_name,
        'mm_aus_str_txt_submit': 'suchen',
    }
    response = requests.post(base_url, headers=headers, data=data)
    selector = Selector(text=response.text)

    return selector.css("div#m_box form div input::attr(value)").get()


def request_calendar(session):
    data = {
        'xxx': '1',
        'mm_ses': session,
        'mm_frm_type': 'termine',
        'mm_frm_fra_SPG': 'SPG',
        'mm_ica_gen': 'iCalendar-Datei laden'
    }
    response = requests.post(base_url, headers=headers, data=data)
    return response.text


def parse_ical(ical_str, street_name):
    ical = Calendar.from_ical(ical_str)
    for component in ical.walk():
        if component.name == 'VEVENT':
            date = component.get('dtstart').dt.strftime("%Y-%m-%d")
            if not date in dates_streetnames:
                dates_streetnames[date] = []
            dates_streetnames[date].append(street_name)


def handle_street_name(street_name):
    # print(f'creating session for {street_name}')
    session = create_session(street_name)
    print(session)

    # print(f'requesting calendar for {street_name}')
    ical = request_calendar(session)
    print(ical)

    # print(f'parsing calendar for {street_name}')
    #parse_ical(ical, street_name)


def generate():
    street_names = request_street_names()
    print(len(street_names))

    sleep_time = 3

    for i in range(len(street_names)):
        print(
            f'{i+1:04}/{len(street_names)} requesting schedule for "{street_names[i]}" ... ', end='', flush=True)
        handle_street_name(street_names[i])
        print('done')
        print(f'sleeping {sleep_time} seconds ... ', end='', flush=True)
        time.sleep(sleep_time)
        print('done')

    with open('data/data.txt', 'w', encoding='utf-8') as outfile:
        json.dump(dates_streetnames, outfile,
                  ensure_ascii=False, sort_keys=True)
    print('All done!')


generate()
