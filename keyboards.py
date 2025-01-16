import cfg, lang

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestUser
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CopyTextButton

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


async def get_main_kb(usrlang: str, player: bool = False) -> ReplyKeyboardMarkup:
    if not player:
        mainkb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=lang.init_promo[usrlang]), KeyboardButton(text=lang.settings[usrlang])],
                [KeyboardButton(text=lang.my_promos[usrlang]), KeyboardButton(text=lang.my_channels[usrlang])]
            ],
            is_persistent = True, resize_keyboard=True
        )
        return mainkb
    mainkb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=lang.my_links[usrlang]), KeyboardButton(text=lang.change_lang[usrlang])],
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
    if not (res := dbrequests.get_upromos_db(uid)):
        return None
    promokb = InlineKeyboardBuilder()
    for row in res:
        promokb.add(InlineKeyboardButton(text=row[1], callback_data=f"forpromo_{row[0]}"))
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


async def get_confirm_inkb(usrlang: str) -> InlineKeyboardMarkup:
    confrmkb = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=lang.confirmpromo[usrlang], callback_data="confirm_promo")
        ]]
    )
    return confrmkb


async def get_postready_inkb(usrlang: str, link: str, channelid: str | int, promoid: str | int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=lang.takepart[usrlang], url=link)],
            [InlineKeyboardButton(text=lang.publish[usrlang], callback_data=f"publish_promo_{channelid}_{link}")],
        ]
    )
    return kb


async def get_link_inkb(text: str, link: str)  -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, url=link)]
        ]
    )
    return kb


async def get_urelfliks_inkb(uid) -> InlineKeyboardMarkup:
    if not (res := dbrequests.get_reflinks(uid)):
        return None
    kb = InlineKeyboardBuilder()
    for row in res:
        kb.add(InlineKeyboardButton(text=row[0], callback_data=f"forreflink_{row[2]}_{row[1]}"))
    return kb.adjust(1).as_markup()


# async def get_copy_inkb(text: str):
#     kb = InlineKeyboardMarkup(
#         [[InlineKeyboardButton(text="copy link", callback_data="ssdf", copy_text=CopyTextButton(text))]]
#     )
#     return kb