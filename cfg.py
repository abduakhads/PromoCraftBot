import envcfg

BOT_TOKEN = envcfg.BOT_TOKEN
UBOT_USERNANE = envcfg.UBOT_USERNAME
UBOT_TOKEN = envcfg.UBOT_TOKEN
WINNER_LOG_CHANNEL = envcfg.WINNER_LOG_CHANNEL
SUPUSERNAME = envcfg.SUPUSERNAME

GUIDE = {
    "en": envcfg.GUIDE["en"],
    "uz": envcfg.GUIDE["uz"],
    "ru": envcfg.GUIDE["ru"]
}


TYPES_GUIDE = {
    "en": envcfg.TYPES_GUIDE["en"],
    "uz": envcfg.TYPES_GUIDE["uz"],
    "ru": envcfg.TYPES_GUIDE["ru"]
}


LANGS = {
    "set_uz": "O'zbekcha",
    "set_ru": "Русский",
    "set_en": "English"
}

PROMO_MODES = {
    "mode_sub": "Subscription",
    "mode_ref": "Referral"
}

SUB_CONF = {
    "confmode_random": "Random",
    # "confmode_list": "List",
}

REF_CONF = {
    "confmode_random": "Random",
    # "confmode_list": "List",
    "confmode_most": "Most"
}


if __name__ == "__main__":
    from database import dbrequests
    dbrequests.setup_tables_db()
    print("done")