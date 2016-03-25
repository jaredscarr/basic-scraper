# -*- coding: utf-8 -*-
import io
import requests
import sys
from bs4 import BeautifulSoup


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


def get_inspection_page(**kwargs):
    """Retrieve the content and encoding from request."""
    url = DOMAIN + PATH
    params = PARAMS
    for key, val in kwargs.items():
        if key in PARAMS:
            params[key] = val
    response = requests.get(url, params=params)
    response.raise_for_status() # <- This is a no-op if there is no HTTP error
    # remember, in requests `content` is bytes and `text` is unicode
    return response.content, response.encoding


def load_inspection_page():
    """Read file from disk and return content and encoding."""
    open_file = io.open('inspection_page.html')
    file = open_file.read()
    open_file.close()
    return file


def parse_source(html):
    parsed = BeautifulSoup(html.encode(), 'html5lib')
    return parsed


def extract_data_listings(parsedhtml):
    """Filter the parsed html."""
    scraped = parsedhtml.find_all('p')
    return scraped


if __name__ == '__main__':
    kwargs = {
        'Inspection_Start': '2/1/2013',
        'Inspection_End': '2/1/2015',
        'Zip_Code': '98109'
    }

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # you will likely have something different here, depending on how
        # you implemented the load_inspection_page function.
        # html = load_inspection_page()
        html, encoding = load_inspection_page('inspection_page.html')
    else:
        html, encoding = get_inspection_page(**kwargs)
    doc = parse_source(html)
    extracted = extract_data_listings(doc)
    print(extracted)
    # doc = parse_source(html, encoding)
    # print doc.prettify(encoding=encoding)

