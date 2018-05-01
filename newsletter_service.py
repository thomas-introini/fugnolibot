import subscription_manager as sm
import newsletter_manager as nlm
import telegramclient as tc
import logging as log

from datetime import datetime
from dateutil import parser


def check_and_notify(nls):
    last_nl = max(nls, key=lambda nl: parser.parse(nl['added_on']))
    added_on_week_nr = parser.parse(last_nl['added_on']).date().isocalendar()[1]
    today_week_nr = datetime.now().date().isocalendar()[1]
    if added_on_week_nr == today_week_nr:
        log.info("Newsletter this week! week number: %s" % today_week_nr)
        nlm.insert_newsletter(
            last_nl['added_on'],
            last_nl['title'],
            last_nl['link']
        )
        subs = sm.get_active_subscriptions()
        if not subs:
            log.info("No active subscription found!")
        else:
            for sub in subs:
                user_id = sub['user_id']
                chat_type = sub['chat_type']
                last_nl_notified = parse_last_nl_notified(sub)
                if last_nl_notified and added_on_week_nr == last_nl_notified:
                    log.info("Sub was already notified, skipping")
                else:
                    send_newsletter_message(last_nl, user_id)
                    sm.update_last_nl_notified(
                        chat_type,
                        user_id,
                        str(today_week_nr)
                    )
    else:
        log.info("Last nl was released on %s, skipping" % last_nl['added_on'])


def send_newsletter_message(nl, user_id):
    tc.send_simple_message(
        user_id,
        "[%s](%s)" % (
            nl['title'],
            nl['link']
        )
    )


def parse_last_nl_notified(sub):
    lnln = sub['last_nl_notified']
    return parser.parse(lnln).date() if lnln else None
