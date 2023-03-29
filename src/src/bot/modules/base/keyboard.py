from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


def build_inlines_menu(buttons: list, pattern) -> ReplyKeyboardMarkup:
    """Построение inline меню в строчку."""
    menu = list()
    for el in buttons:
        menu.append(
            [
                InlineKeyboardButton(
                    el if el else "Не указано",
                    callback_data=pattern + el,
                )
            ]
        )

    return InlineKeyboardMarkup(menu, resize_keyboard=True)
