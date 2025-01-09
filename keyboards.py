import cfg, lang

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUser
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from database import dbrequests


async def get_lang_inkb(langs: dict = cfg.LANGS) -> InlineKeyboardMarkup:
    langkb = InlineKeyboardBuilder()
    for _k, _v in langs.items():
        langkb.add(InlineKeyboardButton(text=_v, callback_data=_k))
    return langkb.adjust(1).as_markup()


async def cancel_all_kb(usrlang: str) -> ReplyKeyboardMarkup:
    cancelkb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=lang.cancel_all[usrlang])]],
        is_persistent = True, resize_keyboard=True
    )
    return cancelkb


async def get_main_kb(usrlang: str) -> ReplyKeyboardMarkup:
    mainkb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=lang.init_promo[usrlang]), KeyboardButton(text=lang.settings[usrlang])],
            [KeyboardButton(text=lang.my_promos[usrlang]), KeyboardButton(text=lang.my_channels[usrlang])]
        ],
        is_persistent = True, resize_keyboard=True
    )
    return mainkb


async def get_prmodes_inkb(prmodes: dict = cfg.PROMO_MODES) -> InlineKeyboardMarkup:
    prmodeskb = InlineKeyboardBuilder()
    for _k, _v in prmodes.items():
        prmodeskb.add(InlineKeyboardButton(text=_v, callback_data=_k))
    return prmodeskb.adjust(1).as_markup()


async def get_prconfmodes_inkb(prmode: str) -> InlineKeyboardMarkup:
    if prmode == "sub":
        prconfmodes = cfg.SUB_CONF
    elif prmode == "ref":
        prconfmodes = cfg.REF_CONF
    prconfmodeskb = InlineKeyboardBuilder()
    for _k, _v in prconfmodes.items():
        prconfmodeskb.add(InlineKeyboardButton(text=_v, callback_data=_k))
    return prconfmodeskb.adjust(1).as_markup()


async def get_uchannels_inkb(uid: int) -> InlineKeyboardMarkup:
    channelskb = InlineKeyboardBuilder()
    for row in dbrequests.load_uchannels_db(uid):
        channelskb.add(InlineKeyboardButton(text=row[1], callback_data=f"forchan_{row[0]}_{row[2]}"))
    return channelskb.adjust(1).as_markup()


async def get_upromos_inkb(uid: int) -> InlineKeyboardMarkup:
    promokb = InlineKeyboardBuilder()
    for row in dbrequests.get_upromos_db(uid):
        promokb.add(InlineKeyboardButton(text=row[1], callback_data=f"forpromo_{row[0]}_{row[1]}"))
    return promokb.adjust(1).as_markup()


async def get_settings_kb(usrlang: str) -> ReplyKeyboardMarkup:
    mainkb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=lang.change_lang[usrlang]), KeyboardButton(text=lang.change_timediff[usrlang])],
            [KeyboardButton(text=lang.cancel_all[usrlang])]
        ],
        is_persistent = True, resize_keyboard=True
    )
    return mainkb