# aspettami-bot

Telegram bot to fetch real-time status and wait time
of Milan's ATM bus and tram lines.

This bot is very much still a work in progress, so
contributions are welcome, as are bug reports and
feature requests.

[Try it live](https://t.me/aspettaMI_bot)

## Run it yourself

```shell
$ docker build -t aspettami-bot:latest .
$ docker run -e "TELEGRAM_TOKEN=<your_tg_token>" -v /path/to/some/data:/usr/src/app/data aspettami-bot:latest
```
