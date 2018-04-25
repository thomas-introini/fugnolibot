from apscheduler.schedulers.background import BlockingScheduler
import telegramclient as tc
import updates_dispatcher as ud
import newsletter_service as nls
import logging as log
import scraper

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
    log.info("Fetching newsletters...")
    newsletters = scraper.scrape_nl()
    nls.check_and_notify(newsletters)


if __name__ == '__main__':
    configure_logger()
    scheduler = BlockingScheduler()
    scheduler.add_job(
        fetch_updates,
        trigger='cron',
        second='*/30'
    )
    scheduler.add_job(
        fetch_nl,
        trigger='cron',
        day_of_week='4-5',  # Thu-Fri (4-5)
        hour='7-19',        # 07:00 - 19:00
        minute='*/10'
    )
    scheduler.start()
