import cfg

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUser
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


async def get_lang_inkb(langs: dict = cfg.LANGS) -> InlineKeyboardMarkup:
    langkb = InlineKeyboardBuilder()
    for _k, _v in langs.items():
        langkb.add(InlineKeyboardButton(text=_v, callback_data=_k))
    return langkb.adjust(1).as_markup()
