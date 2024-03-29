import os

API_URL = "https://giromilano.atm.it/proxy.ashx"
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", None)
