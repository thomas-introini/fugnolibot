from bs4 import BeautifulSoup
import urllib.request
import logging as log
import os

USE_TEST_PAGE = os.getenv("FUGNOLI_BOT_USE_TEST_PAGE", "True") == "True"
page_name = os.getenv("FUGNOLI_BOT_NL_PAGE", "foo")


def scrape_nl():
    html = get_page()
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.find_all('div', class_='rassegna-stampa-element', limit=5)
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
        with open('test/nl_kairos.html') as f:
            return f.read()
    else:
        req = urllib.request.Request(
            page_name,
            data=None,
            headers={
                'User-Agent': '''Mozilla/5.0 (X11; Linux x86_64; rv:57.0)
                Gecko/20100101 Firefox/57.0'''
            }
        )
        with urllib.request.urlopen(req) as page:
            return page.read().decode('utf-8')
