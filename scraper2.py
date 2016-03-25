import io
import re
import requests
from bs4 import BeautifulSoup
import sys


DOMAIN = 'http://info.kingcounty.gov'
PATH = '/health/ehs/foodsafety/inspections/Results.aspx'
PARAMS = {
    'Output': 'W',
    'Business_Name': '',
    'Business_Address': '',
    'Longitude': '',
    'Latitude': '',
    'City': '',
    'Zip_Code': '',
    'Inspection_Type': 'All',
    'Inspection_Start': '',
    'Inspection_End': '',
    'Inspection_Closed_Business': 'A',
    'Violation_Points': '',
    'Violation_Red_Points': '',
    'Violation_Descr': '',
    'Fuzzy_Search': 'N',
    'Sort': 'H'
}

TEST_HTML = 'inspection_page.html'


def get_inspection_page(**kwargs):
    url = DOMAIN + PATH
    params = PARAMS.copy()
    for key, val in kwargs.items():
        if key in PARAMS:
            params[key] = val
    resp = requests.get(url, params=params)
    resp.raise_for_status() # <- This is a no-op if there is no HTTP error
    # remember, in requests `content` is bytes and `text` is unicode
    return resp.content, resp.encoding


def parse_source(html, encoding='utf-8'):
    if isinstance(html, bytes):
        parsed = BeautifulSoup(html, 'html5lib', from_encoding=encoding)
    else:
        parsed = BeautifulSoup(html, 'html5lib')
    return parsed


def load_inspection_page(file):
    open_file = io.open(file)
    file = open_file.read()
    open_file.close()
    return file, 'utf-8'


def extract_data_listings(html):
    id_finder = re.compile(r'PR[\d]+~')
    return html.find_all('div', id=id_finder)


def has_two_tds(elem):
    is_tr = elem.name == 'tr'
    td_children = elem.find_all('td', recursive=False)
    has_two = len(td_children) == 2
    return is_tr and has_two


def clean_data(td):
    data = td.string
    try:
        return data.strip(" \n:-")
    except AttributeError:
        return u""


if __name__ == '__main__':
    kwargs = {
        'Inspection_Start': '2/1/2013',
        'Inspection_End': '2/1/2015',
        'Zip_Code': '98109'
    }
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = load_inspection_page(TEST_HTML)
    else:
        html, encoding = get_inspection_page(**kwargs)
    doc = parse_source(html, encoding)
    listings = extract_data_listings(doc)
    for listing in listings[:5]:
        metadata_rows = listing.find('tbody').find_all(
            has_two_tds, recursive=False
        )
        for row in metadata_rows:
            for td in row.find_all('td', recursive=False):
                print(clean_data(td)),
            print
        print

