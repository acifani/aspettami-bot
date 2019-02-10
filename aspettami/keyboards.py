from typing import List, Union

from telegram import InlineKeyboardMarkup, InlineKeyboardButton as Button

from aspettami.stop import Stop


def build_stops_buttons(stops: List[Stop]) -> List[List[Button]]:
    return [
        [buttonize_stop(stop)]
        for stop in stops
        # only include buses and trams
        if stop.is_bus_or_tram_stop()
    ]


def build_stops_keyboard(stops: List[Stop]) -> InlineKeyboardMarkup:
    buttons = build_stops_buttons(stops)
    return InlineKeyboardMarkup(buttons)


def buttonize_stop(stop: Stop) -> Button:
    text = f"{stop.get_name()}"
    data = f"#{stop.get_code()}"
    return Button(text, callback_data=data)


def build_line_stop_keyboard(
    stop_code: Union[int, str], is_fav: bool
) -> InlineKeyboardMarkup:
    refresh = Button("🔃 Refresh", callback_data=f"#{stop_code}")

    if is_fav:
        fav = Button("💔 Remove from favs", callback_data=f"-{stop_code}")
    else:
        fav = Button("❤ Add to favs", callback_data=f"+{stop_code}")

    return InlineKeyboardMarkup([[fav, refresh]])


def build_favs_keyboard() -> InlineKeyboardMarkup:
    refresh = Button("🔃 Refresh", callback_data=f"favs")
    return InlineKeyboardMarkup([[refresh]])
