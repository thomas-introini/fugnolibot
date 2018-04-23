import subscription_manager as sm
import telegramclient as tc
import logging as log

from datetime import datetime
from dateutil import parser


def check_and_notify(nls):
    last_nl = max(nls, key=lambda nl: parser.parse(nl['added_on']))
    added_on = parser.parse(last_nl['added_on']).date()
    today = datetime.now().date()
    if added_on == today:
        log.info("Newsletter added today!")
        subs = sm.get_active_subscriptions()
        if not subs:
            log.info("No active subscription found!")
        else:
            for sub in subs:
                user_id = sub['user_id']
                last_nl_notified = parse_last_nl_notified(sub)
                if last_nl_notified and added_on == last_nl_notified:
                    log.info("Sub was already notified, skipping")
                else:
                    tc.send_simple_message(
                        user_id,
                        "[%s](%s)" % (
                            last_nl['title'],
                            last_nl['link']
                        )
                    )
                    sm.update_last_nl_notified(
                        user_id,
                        str(today)
                    )
    else:
        log.info("Last nl was released on %s, skipping" % added_on)


def parse_last_nl_notified(sub):
    lnln = sub['last_nl_notified']
    return parser.parse(lnln).date() if lnln else None
