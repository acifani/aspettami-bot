from telegram.ext import Updater

import aspettami.handlers as handlers
from aspettami.config import TELEGRAM_TOKEN
from aspettami.logger import logger


def start():
    logger.info("Bot starting...")
    if TELEGRAM_TOKEN is None:
        raise ValueError("TELEGRAM_TOKEN not set")
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(handlers.start_handler_builder())
    dp.add_handler(handlers.stop_info_handler_builder())
    dp.add_handler(handlers.stop_search_handler_builder())
    dp.add_handler(handlers.get_fav_handler_builder())
    dp.add_handler(handlers.add_fav_handler_builder())
    dp.add_handler(handlers.del_fav_handler_builder())
    dp.add_error_handler(handlers.error_handler)

    updater.start_polling()
    logger.info("Bot started")
    updater.idle()
    logger.info("Bot shutting down")
