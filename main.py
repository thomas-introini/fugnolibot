import telegramclient as tc
import updates_dispatcher as ud
import newsletter_service as nls
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
    newsletters = scraper.scrape_nl()
    nls.check_and_notify(newsletters)


if __name__ == '__main__':
    configure_logger()
    schedule.every(10).seconds.do(fetch_updates)
    schedule.every(10).seconds.do(fetch_nl)
    while True:
        schedule.run_pending()
        time.sleep(1)
