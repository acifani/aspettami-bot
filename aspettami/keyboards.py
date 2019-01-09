from typing import List

from telegram import InlineKeyboardMarkup, InlineKeyboardButton as Button

from aspettami.stop import Stop


def build_stops_keyboard(stops) -> InlineKeyboardMarkup:
    buttons = build_stops_buttons(stops)
    return InlineKeyboardMarkup(buttons)


def build_stops_buttons(stops: List[Stop]):
    return [
        [buttonize_stop(stop)]
        for stop in stops
        # only include buses and trams
        if stop.is_bus_or_tram_stop()
    ]


def buttonize_stop(stop: Stop):
    text = f"{stop.get_name()}"
    data = f"#{stop.get_code()}"
    return Button(text, callback_data=data)


def build_line_stop_keyboard(stop: Stop):
    # back = Button("🔙 Back", callback_data="back")
    refresh = Button("🔃 Refresh", callback_data=f"#{stop.get_code()}")
    # timetable = Button("⏲ Timetable", url="https://google.com")
    return InlineKeyboardMarkup([[refresh]])
