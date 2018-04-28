import logging as log
import telegramclient as tc
import subscription_manager as sm


def dispatch(update):
    update_id = update['update_id']
    message = update['message']
    if 'entities' in message and filter(lambda e: e['type'] == 'bot_command', message['entities']):
        process_command(update_id, message)
    else:
        process_text(update_id, message)


def process_command(update_id, message):
    command_string = message['text']
    command_split = command_string.split(' ')
    command_to_bot = command_split[0]
    command = command_to_bot.split('@')
    if len(command) > 1 and command[1] != 'fugnoliBot':
        log.info("Ignoring bot command since it's not for me")
    elif command[0] in command_types:
        command_types[command[0]](update_id, message, command_split[1:])
    else:
        log.error('Unknown command...')
        process_unknown(update_id, message)


def process_unknown(update_id, message):
    user_id, chat_type = get_subscriber_info(message)
    tc.send_simple_message(
        user_id,
        "Mmmm tigre, non conosco questo comando, ma non ti preoccupare, non smetto mai di imparare"
    )


def process_text(update_id, message):
    user_id, chat_type = get_subscriber_info(message)
    if chat_type == 'private':
        tc.send_simple_message(
            user_id,
            "Non smettere mai di essere te stesso ;)"
        )


def process_start(update_id, message, args):
    log.info("process start")


def process_subscribe(update_id, message, args):
    log.info("process subscribe")
    user_id, chat_type = get_subscriber_info(message)
    if sm.is_subscription_active(chat_type, user_id):
        tc.send_simple_message(
            user_id,
            "Aspetta un attimo tigre... sembra che tu sia già iscritto..."
        )
    else:
        try:
            sm.insert_subscription(chat_type, user_id, message)
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
    user_id, chat_type = get_subscriber_info(message)
    message = "Tigre, non sei nemmeno iscritto e vorresti disiscriverti?"
    if sm.is_subscription_active(chat_type, user_id):
        if sm.deactivate_subscription(chat_type, user_id):
            message = "Ci mancherai tigre..."
        else:
            message = "Non sono riuscito a disiscriverti tigre..."
    tc.send_simple_message(user_id, message)


def get_subscriber_info(message):
    chat_type = message['chat']['type']
    user_id = message['from']['id'] if chat_type == 'private' else message['chat']['id']
    return (user_id, chat_type)


command_types = {
    '/start': process_start,
    '/subscribe': process_subscribe,
    '/unsubscribe': process_unsubscribe
}
