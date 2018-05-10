from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from dateutil import parser
from datetime import datetime

import telegramclient as tc
import updates_dispatcher as ud
import newsletter_service as nls
import newsletter_manager as nlm
import logging as log
import scraper
import os

UPDATES_CRON = os.getenv(
    'FUGNOLI_BOT_UPDATES_CRON',
    "*/15 * * * * * *"
)
NL_FETCH_CRON = os.getenv(
    'FUGNOLI_BOT_NL_FETCH_CRON',
    "0 0/10 7-19 * * thu-fri *"
)

LOG_FORMATTER = log.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")


def configure_logger():
    rootLogger = log.getLogger()

    fileHandler = log.FileHandler("fugnolibot.log")
    fileHandler.setFormatter(LOG_FORMATTER)
    rootLogger.addHandler(fileHandler)

    consoleHandler = log.StreamHandler()
    consoleHandler.setFormatter(LOG_FORMATTER)
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
    last_nl = nlm.get_last_newsletter()
    if last_nl is not None:
        now = datetime.now()
        dt = parser.parse(last_nl['date']).date()
        week_number = dt.isocalendar()[1]
        now_week_number = now.isocalendar()[1]
        log.info("Last nl week: %d, current week: %d" % (week_number, now_week_number))
        if week_number != now_week_number:
            scrape_and_notify()
        else:
            log.info("Newsletter already found this week, skipping")
    else:
        log.info("No last nl was found, scraping...")
        scrape_and_notify()


def scrape_and_notify():
    newsletters = scraper.scrape_nl()
    nls.check_and_notify(newsletters)


def get_cron_trigger(expr):
    log.info("Creating crono trigger with %s" % expr)
    values = expr.split()
    if len(values) < 7:
        raise ValueError(
            "Wrong number of fields; got {}, expected 7"
            .format(len(values))
        )

    return CronTrigger(
        second=values[0],
        minute=values[1],
        hour=values[2],
        day=values[3],
        month=values[4],
        day_of_week=values[5],
        year=values[6]
    )


def get_cron_triggers(exprs):
    return [get_cron_trigger(e) for e in exprs.split(';')]


if __name__ == '__main__':
    configure_logger()
    scheduler = BlockingScheduler()
    for ct in get_cron_triggers(UPDATES_CRON):
        scheduler.add_job(
            fetch_updates,
            ct
        )
    for ct in get_cron_triggers(NL_FETCH_CRON):
        scheduler.add_job(
            fetch_nl,
            ct
        )
    scheduler.start()
