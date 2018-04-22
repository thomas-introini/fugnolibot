from dateutil import parser
from datetime import now
import telegramclient as tc
import updates_dispatcher as ud
import logging as log
import schedule
import scraper
import time

logFormatter = log.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")


def configure_logger():
    rootLogger = log.getLogger()

    fileHandler = log.FileHandler("fugnolibot.log")
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = log.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    rootLogger.setLevel("DEBUG")


def fetch_updates():
    updates = tc.get_updates()
    log.info("Fetching updates...")
    for u in updates:
        id = u["update_id"]
        log.info(u)
        ud.dispatch(u)
        tc.set_offset(id + 1)


def fetch_nl():
    nls = scraper.scrape_nl()
    last_nl = max(nls, key=lambda nl: parser.parse(nl['added_on']))
    added_on = parser.parse(last_nl['added_on']).date()
    today = now().date()
    if added_on == today:
        pass
    else:
        pass


if __name__ == '__main__':
    configure_logger()
    fetch_nl()
    # schedule.every(10).seconds.do(fetch_updates)
    # schedule.every(10).seconds.do(fetch_nl)
    # while True:
    #    schedule.run_pending()
    #    time.sleep(1)
