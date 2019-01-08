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

    dp.add_handler(handlers.start_handler())
    dp.add_handler(handlers.stop_info_handler())
    dp.add_handler(handlers.stop_search_handler())
    dp.add_error_handler(handlers.error_handler)

    updater.start_polling()
    updater.idle()
