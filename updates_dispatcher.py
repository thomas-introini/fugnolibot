import logging as log
import telegramclient as tc
import subscription_manager as sm


def dispatch(update):
    update_id = update['update_id']
    message = update['message']
    entities = message['entities']
    if filter(lambda e: e['type'] == 'bot_command', entities):
        process_command(update_id, message)
    else:
        process_text(update_id, message)


def process_command(update_id, message):
    command_string = message['text']
    command_split = command_string.split(' ')
    command = command_split[0]
    if command in command_types:
        command_types[command](update_id, message, command_split[1:])
    else:
        log.error('Unknown command...')
        # Report to user


def process_text(update_id, message):
    log.info("process text")


def process_start(update_id, message, args):
    log.info("process start")


def process_subscribe(update_id, message, args):
    log.info("process subscribe")
    user_id = message['from']['id']
    if sm.is_subscription_active(user_id):
        tc.send_simple_message(
            user_id,
            "Aspetta un attimo tigre... sembra che tu sia già iscritto..."
        )
    else:
        try:
            sm.insert_subscription(user_id, message)
            tc.send_simple_message(
                user_id,
                "Complimenti tigre! Sei iscritto!"
            )
        except Exception as e:
            log.error(str(e))
            tc.send_simple_message(
                user_id,
                """Mmmm... sembra che qualcosa sia andato storto tigre...
                   non sono riuscito ad iscriverti..."""
            )


def process_unsubscribe(update_id, message, args):
    log.info("process unsubscribe")
    user_id = message['from']['id']
    message = "Tigre, non sei nemmeno iscritto e vorresti disiscriverti?"
    if sm.is_subscription_active(user_id):
        if sm.deactivate_subscription(user_id):
            message = "Ci mancherai tigre..."
        else:
            message = "Non sono riuscito a disiscriverti tigre..."
    tc.send_simple_message(user_id, message)


command_types = {
    '/start': process_start,
    '/subscribe': process_subscribe,
    '/unsubscribe': process_unsubscribe
}
