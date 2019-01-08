from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler
from telegram.ext.filters import Filters

import aspettami.api as api
from aspettami.logger import logger


def start_handler() -> CommandHandler:
    return CommandHandler("start", _start)


def stop_search_handler() -> MessageHandler:
    return MessageHandler(Filters.text, _stop_search)


def stop_info_handler() -> CallbackQueryHandler:
    return CallbackQueryHandler(_stop_info, pattern=r"#[\d+]")


def error_handler(bot: Bot, update: Update, error: str):
    logger.warn(f"Update {update} caused error {error}")


def _start(bot: Bot, update: Update):
    update.message.reply_text(
        "Hey there! Start looking for stops by sending me a name or a code"
    )


def _stop_search(bot: Bot, update: Update):
    response = api.search_stop(update.message.text)

    markup = None
    message = None
    if not len(response):
        message = "Could not find any stop"
    else:
        get_description = lambda stop: f'{stop["CustomerCode"]} - {stop["Description"]}'
        stops = [
            [
                InlineKeyboardButton(
                    get_description(stop), callback_data=f'#{stop["Code"]}'
                )
            ]
            for stop in response
        ]
        markup = InlineKeyboardMarkup(stops)
        message = "Pick a stop"

    update.message.reply_text(message, reply_markup=markup)


def _stop_info(bot: Bot, update: Update):
    query = update.callback_query
    stop_code = query.data[1:].strip()
    response = api.get_stop_info(stop_code)

    if response:
        message = _transform_stop(response)
    else:
        message = "Could not find any stop"

    bot.edit_message_text(
        chat_id=query.message.chat_id, message_id=query.message.message_id, text=message
    )


def _transform_stop(stop):
    stop_info = "\n\n".join([_transform_line(line) for line in stop["Lines"]])
    return f'Stop: {stop["Description"]}\n{stop_info}'


def _transform_line(line):
    return (
        f'Line: {line["Line"]["LineCode"]} - {line["Line"]["LineDescription"]}\n'
        f'Time left: {line["WaitMessage"]}'
    )
