from bs4 import BeautifulSoup
import urllib.request
import logging as log
import os

USE_TEST_PAGE = os.getenv("FUGNOLI_BOT_USE_TEST_PAGE", "True") == "True"
PAGE_NAME = os.environ.get("FUGNOLI_BOT_NL_PAGE")
TEST_PAGE_PATH = os.environ.get("FUGNOLI_BOT_NL_TEST_PAGE_PATH")


def scrape_nl():
    html = get_page()
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.find_all('div', class_='rassegna-stampa-element')
    log.info("Found %d elements" % len(elements))
    nls = []
    for element in elements:
        link = element.find('a')
        span = element.find('span', class_='date-display-single')
        nls.append({
            'added_on': span['content'],
            'link': link['href'],
            'title': link.text
        })
    return nls


def get_page():
    if USE_TEST_PAGE:
        with open(TEST_PAGE_PATH) as f:
            return f.read()
    else:
        log.info("Requesting URL: %s" % PAGE_NAME)
        req = urllib.request.Request(
            PAGE_NAME,
            data=None,
            headers={
                'User-Agent': '''Mozilla/5.0 (X11; Linux x86_64; rv:57.0)
                Gecko/20100101 Firefox/57.0'''
            }
        )
        with urllib.request.urlopen(req) as page:
            return page.read().decode('utf-8')
