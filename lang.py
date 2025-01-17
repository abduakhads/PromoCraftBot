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
    "en": "Choose one of active promos:"
}


async def promo_info(usrlang: str, promo_id, mode, exp, inv, par, joins, title, winners):
    info = {
        "ref": {
            "en": f"*Promo ID:* {promo_id}\n*Title:* {title}\n*Mode:* Referal {mode.split('_')[1]}\n*Expires:* {exp}\n*Should invite (for random submode only):* {inv}\n\n*Participants:* {par}\n*New joins:* {joins}\n\n*Number of winners:* {winners}"
        },
        "sub": {
            "en": f"*Promo ID:* {promo_id}\n*Title:* {title}\n*Mode:* Subscription {mode.split('_')[1]}\n*Expires:* {exp}\n\n*Participants:* {par}\n\n*Number of winners:* {winners}"
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


ref_joined = {
    "en": "joined via your"
}


ref_left = {
    "en": "left channel"
}


choose_lang = {
    "en": "Please choose language"
}


give_ur_time = {
    "en": "Please give your current date and time in format:\ndd.mm.yyyy hh:mm"
}


choose_option = {
    "en": "Please choose one option"
}


need_conf_tim = {
    "en": "You need to configure time zone first"
}


lets_start = {
    "en": "Let's start!"
}


select_channel = {
    "en": "Choose one of the channels:"
}


no_channel = {
    "en": "Please add me to channel first"
}


give_title = {
    "en": "Give a title for promo:"
}


choose_mode = {
    "en": "Choose the mode\n\nmore info -> link",
}


choose_submode = {
    "en": "Choose the sub mode\n\nmore info -> link"
}


invite_numb = {
    "en": "Give the numbers of users participants should invite"
}


winners_numb = {
    "en": "Give the number of winners"
}


give_int = {
    "en": "Please provide integer number!"
}


give_exp = {
    "en": "Give the expiry date and time in format dd.mm.yyyy hh:mm"
}

async def is_correct(usrlang, title, mode, exp, inv, winners):
    info = {
        "ref": {
            "en": f"Check if everything is correct\n\n*Title:* {title}\n*Mode:* Referal {mode.split('_')[1]}\n*Expires:* {exp}\n*Should invite (for random submode only):* {inv}\n\n*Number of winners:* {winners}"
        },
        "sub": {
            "en": f"Check if everything is correct\n\n*Title:* {title}\n*Mode:* Subscription {mode.split('_')[1]}\n*Expires:* {exp}\n\n*Number of winners:* {winners}"
        }
    }
    return info[mode.split('_')[0]][usrlang]


give_post = {
    "en": "Now send me your post that will be shared (published)"
}


published = {
    "en": "published to channel"
}


promo_exp = {
    "en": "The promo expired or does not exist"
}


sub_first = {
    "en": "Please subscribe to channel first. "
}


ur_reflink = {
    "en": "Here is your referal link (via which you can invite) "
}


done_par = {
    "en": "Done you are participant"
}


no_reflinks = {
    "en": "You do not have any active referal links"
}


async def inv_info(usrlang, joined, link):
    res = {
        "en": f"People joined: {joined}\n\nLink: {link}"
    }
    return res[usrlang]


async def no_winners(usrlang, promo, plcount, joincount):
    res = {
        "en": f"There is no winners on promo: {promo}\n\nParticipated: {plcount}\nNew joins: {joincount}"
    }
    return res[usrlang]


winners_an =  {
    "en": "winners_check results"
}