from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def good_kb():
    del_btn = InlineKeyboardButton("Удалить.", callback_data="delete_this_shit")
    return InlineKeyboardMarkup().add(del_btn)