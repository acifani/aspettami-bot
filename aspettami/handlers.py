from telegram import Bot, Update, ParseMode
from telegram.error import BadRequest
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler
from telegram.ext.filters import Filters

import aspettami.api as api
from aspettami import db
from aspettami.keyboards import build_stops_keyboard, build_line_stop_keyboard
from aspettami.logger import logger


def start_handler_builder() -> CommandHandler:
    return CommandHandler("start", start_handler)


def stop_search_handler_builder() -> MessageHandler:
    return MessageHandler(Filters.text, stop_search_handler)


def stop_info_handler_builder() -> CallbackQueryHandler:
    return CallbackQueryHandler(stop_info_handler, pattern=r"#[\d]+")


def get_fav_handler_builder() -> CommandHandler:
    return CommandHandler("favs", get_fav_handler)


def add_fav_handler_builder() -> CallbackQueryHandler:
    return CallbackQueryHandler(add_fav_handler, pattern=r"\+[\d]+")


def del_fav_handler_builder() -> CallbackQueryHandler:
    return CallbackQueryHandler(del_fav_handler, pattern=r"-[\d]+")


def error_handler(bot: Bot, update: Update, error: str):
    logger.warn(f"Update {update} caused error {error}")


def start_handler(bot: Bot, update: Update):
    update.message.reply_text(
        "Hey there! Start looking for stops by sending me a name or a code"
    )


def stop_search_handler(bot: Bot, update: Update):
    message, markup = stop_search(update.message.text, update.message.chat_id)
    update.message.reply_text(
        message, reply_markup=markup, parse_mode=ParseMode.MARKDOWN
    )


def stop_search(user_query: str, user: int):
    stops = api.search_stop(user_query)
    if len(stops) == 1:
        stop_code = stops[0].get_code()
        message, markup = stop_info(stop_code, db.is_fav(user, stop_code))
    elif stops:
        message = f'_🔍 {len(stops)} stops found for "{user_query}"_\n\n'
        message += "\n\n".join([stop.get_overview() for stop in stops])
        markup = build_stops_keyboard(stops)
    else:
        message = "Could not find any stop"
        markup = None
    return message, markup


def stop_info_handler(bot: Bot, update: Update):
    query = update.callback_query
    stop_code = query.data[1:].strip()
    message, markup = stop_info(stop_code, db.is_fav(query.message.chat_id, stop_code))
    try:
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=message,
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
    except BadRequest:
        # Message is not modified
        bot.answer_callback_query(query.id)


def stop_info(stop_code: str, is_fav: bool):
    stop = api.get_stop_info(stop_code)
    if stop:
        message = stop.get_overview()
        markup = build_line_stop_keyboard(stop, is_fav)
    else:
        message = "Could not find any stop"
        markup = None
    return message, markup


def get_fav_handler(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    favs = db.get_fav(chat_id)
    messages = [api.get_stop_info(str(stop_code)).get_overview() for stop_code in favs]
    message = "\n".join(messages) if messages else "🙄 You have no favorites"

    bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN)


def add_fav_handler(bot: Bot, update: Update):
    query = update.callback_query
    stop_code = query.data[1:].strip()
    user = query.message.chat_id
    db.add_fav(user, stop_code)

    message, markup = stop_info(stop_code, True)
    try:
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=message,
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
    except BadRequest:
        # Message is not modified
        bot.answer_callback_query(query.id)


def del_fav_handler(bot: Bot, update: Update):
    query = update.callback_query
    stop_code = query.data[1:].strip()
    user = query.message.chat_id
    db.del_fav(user, stop_code)

    message, markup = stop_info(stop_code, False)
    try:
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=message,
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
    except BadRequest:
        # Message is not modified
        bot.answer_callback_query(query.id)
