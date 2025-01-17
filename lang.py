set_lang_done = {
    "uz": "O'zbek tili tanlandi",
    "ru": "Выбран русский язык",
    "en": "Chosen English language" 
}


change_lang = {
    "en": "Language",
    "uz": "Til",
    "ru": "Язык"
}


cancel_all = {
    "en": "Cancel",
    "uz": "Bekor qilish",
    "ru": "Отменить"
}

cancel_done = {
    "en": "Canceled"
}


init_promo = {
    "en": "Create promo"
}


my_channels = {
    "en": "My channels"
}


my_promos = {
    "en": "My promos"
}


change_timediff = {
    "en": "Time zone"
}


settings = {
    "en": "Settings"
}


confirmpromo = {
    "en": "Correct"
}


takepart = {
    "en": "Participate"
}


publish = {
    "en": "Publish to channel"
}


my_links = {
    "en": "My links"
}


no_promos = {
    "en": "You do not have any active promos"
}


on_promos = {
    "en": "Here are your active promos:"
}


async def promo_info(usrlang: str, promo_id, mode, exp, inv, par, joins):
    info = {
        "ref": {
            "en": f"*Promo ID:* {promo_id}\n*Mode:* Referal {mode.split('_')[1]}\n*Expires:* {exp}\n*Should invite (for random mode only):* {inv}\n\n*Participants:* {par}\n*New joins:* {joins}"
        },
        "sub": {
            "en": f"*Promo ID:* {promo_id}\n*Mode:* Subscription {mode.split('_')[1]}\n*Expires:* {exp}\n\n*Participants:* {par}"
        }
    }
    return info[mode.split('_')[0]][usrlang]


on_channels = {
    "en": "Here are your channels with me having correct rights\n\n"
}


no_channels = {
    "en": "You did not add me to any channels!"
}


added_channel = {
    "en": "Added channel "
}


async def edited_ch_from(usrlang: str, title: str, link: str):
    txt = {
        "en": f"Please give the admin rights mentioned in guide for channel: [{title}]({link}),\
            \n\notherwise bot can't publish results or genereate links to channel"
    }
    return txt[usrlang]


async def kicked_from_ch(usrlang: str, title: str, link: str):
    txt = {
        "en": f"Bot was kicked from [{title}]({link}),\nyour promos related to channel are deleted",
    }
    return txt[usrlang]


promo_canceled = {
    "en": "Promo was calceled in channel "
}