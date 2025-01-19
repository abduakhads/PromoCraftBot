set_lang_done = {
    "uz": "O'zbek tili tanlandi",
    "ru": "Выбран русский язык",
    "en": "Chosen English language" 
}


change_lang = {
    "en": "🌐 Language",
    "uz": "🌐 Til",
    "ru": "🌐 Язык"
}


cancel_all = {
    "en": "⬅️ Cancel",
    "uz": "⬅️ Bekor qilish",
    "ru": "⬅️ Отменить"
}

cancel_done = {
    "en": "Canceled",
    "uz": "Bekor qilindi",
    "ru": "Отменен"
}


init_promo = {
    "en": "🎁 Create promo",
    "uz": "🎁 Promo yaratish",
    "ru": "🎁 Создать промо"
}


my_channels = {
    "en": "📢 My channels",
    "uz": "📢 Kanallarim",
    "ru": "📢 Мои каналы"
}


my_promos = {
    "en": "🗓 My promos",
    "uz": "🗓 Promolarim",
    "ru": "🗓 Мои промо"
}


change_timediff = {
    "en": "⏳ Time zone",
    "uz": "⏳ Vaqt mintaqasi",
    "ru": "⏳ Часовой пояс"
}


settings = {
    "en": "⚙️ Settings",
    "uz": "⚙️ Sozlamalar",
    "ru": "⚙️ Настройки"
}


confirmpromo = {
    "en": "Correct ✅",
    "uz": "To'g'ri ✅",
    "ru": "Правильно ✅"

}


takepart = {
    "en": "Participate 🚀",
    "uz": "Ishtirok etish 🚀",
    "ru": "Участвовать 🚀"
}


publish = {
    "en": "Publish to channel",
    "uz": "Kanalda e'lon qilish",
    "ru": "Опубликовать на канале"
}


my_links = {
    "en": "🔗 My links",
    "uz": "🔗 Havolalarim",
    "ru": "🔗 Мои ссылки"
}


no_promos = {
    "en": "You do not have any active promos",
    "uz": "Sizda faol promolar yo'q",
    "ru": "У вас нет активных промо"
}


on_promos = {
    "en": "Choose one of active promos:",
    "uz": "Faol promolardan birini tanlang:",
    "ru": "Выберите одну из активных промо:"
}


async def promo_info(usrlang: str, promo_id, mode, exp, inv, par, joins, title, winners):
    info = {
        "ref": {
            "en": f"*Promo ID:* {promo_id}\n*Title:* {title}\n*Type:* Referral {mode.split('_')[1]}\n*Expires:* {exp}\n*Should invite (for random sub mode only):* {inv}\n\n*Participants:* {par}\n*New joins:* {joins}\n\n*Number of winners:* {winners}",
            "uz": f"*Promo ID:* {promo_id}\n*Sarlavhasi:* {title}\n*Turi:* Referral {mode.split('_')[1]}\n*Tugash muddati:* {exp}\n*Taklif qilish kerak (faqat random rejim uchun):* {inv}\n\n*Ishtirokchilar:* {par}\n*Yangi qo'shilganlar:* {joins}\n\n*G'oliblar soni:* {winners}",
            "ru": f"*Промо ID:* {promo_id}\n*Заголовок:* {title}\n*Тип:* Referral {mode.split('_')[1]}\n*Истекает:* {exp}\n*Нужно пригласить (только для рандом режима):* {inv}\n\n*Участники:* {par}\n*Новые подписчики:* {joins}\n\n*Количество победителей:* {winners}"
        },
        "sub": {
            "en": f"*Promo ID:* {promo_id}\n*Title:* {title}\n*Mode:* Subscription {mode.split('_')[1]}\n*Expires:* {exp}\n\n*Participants:* {par}\n\n*Number of winners:* {winners}",
            "uz": f"*Promo ID:* {promo_id}\n*Sarlavhasi:* {title}\n*Turi:* Subscription {mode.split('_')[1]}\n*Tugash muddati:* {exp}\n\n*Ishtirokchilar:* {par}\n\n*G'oliblar soni:* {winners}",
            "ru": f"*Промо ID:* {promo_id}\n*Заголовок:* {title}\n*Тип:* Subscription {mode.split('_')[1]}\n*Истекает:* {exp}\n\n*Участники:* {par}\n\n*Количество победителей:* {winners}"
        }
    }
    return info[mode.split('_')[0]][usrlang]


on_channels = {
    "en": "Here are your channels with me having correct rights\n\n",
    "uz": "Meni quyidagi kanallarga qo'shgansiz va kerakli huquqlarni bergansiz\n\n",
    "ru": "Вы добавили меня в следующие каналы и предоставили необходимые права\n\n"
}


no_channels = {
    "en": "You did not add me to any channels (or did not give right permissions)!",
    "uz": "Meni hech qanday kanalga qo'shmadingiz (yoki zarur huquqlarni bermadingiz)!",
    "ru": "Вы не добавили меня ни в один канал (или не дали нужных разрешений)!"
}


added_channel = {
    "en": "Added channel ",
    "uz": "Quyidagi kanal qo'shildi ",
    "ru": "Добавлен канал "
}


async def edited_ch_from(usrlang: str, title: str, link: str):
    txt = {
        "en": f"Please give the admin rights mentioned in guide for channel: [{title}]({link}),\
            \n\notherwise bot can't publish results or generate links to channel",
        "uz": f"Iltimos botga quyidagi kanalda qo'llanmada keltirilgan huquqlarni bering: [{title}]({link}),\
            \n\naks holda bot g'oliblarni e'lon qila olmaydi yoki kanal uchun havola yarata olmaydi",
        "ru": f"Пожалуйста, предоставьте права администратора боту, указанные в руководстве для канала: [{title}]({link}),\
            \n\nв противном случае бот не сможет публиковать результаты или генерировать ссылки на канал"
    }
    return txt[usrlang] #TODO add links


async def kicked_from_ch(usrlang: str, title: str, link: str):
    txt = {
        "en": f"Bot was kicked from [{title}]({link}),\nyour promos related to channel are deleted",
        "uz": f"Bot [{title}]({link}) kanaldan chiqarib yuborildi, kanalning barcha promolari o'chirib yuborildi",
        "ru": f"Бот был выкинут из [{title}]({link}),\nваши промо, связанные с каналом, удалены"
    }
    return txt[usrlang]


promo_canceled = {
    "en": "Promo was calceled in channel ",
    "uz": "Quyidagi kanalda promo bekor qilindi",
    "ru": "Промо было отменено в канале "
}


ref_joined = {
    "en": "joined channel via your",
    "uz": "sizning quyidagi havolangiz orqali kanalga qo'shildi",
    "ru": "присоединился в канал по вашей следующей ссылке"
}


ref_left = {
    "en": "left channel",
    "uz": "kanaldan chiqib ketdi",
    "ru": "покинул канал"
}


choose_lang = {
    "en": "Please choose language",
    "uz": "Iltimos tilni tanlang",
    "ru": "Пожалуйста, выберите язык"
}


give_ur_time = {
    "en": "Please give your current date and time in format:\ndd.mm.yyyy hh:mm",
    "uz": "Hozirgi sana va vaqtingizni quyidagi formatda kiriting:\nkun.oy.yil soat:daqiqa",
    "ru": "Укажите текущую дату и время в формате:\nдд.мм.гггг чч:мм"
}


choose_option = {
    "en": "Please choose one option",
    "uz": "Iltimos, quyidagilarning birini tanlang",
    "ru": "Пожалуйста, выберите один из опций"
}


need_conf_tim = {
    "en": "You need to configure time zone first",
    "uz": "Avval vaqt mintaqasini sozlashingiz kerak",
    "ru": "Сначала вам нужно настроить часовой пояс"
}


lets_start = {
    "en": "Let's start!",
    "uz": "Boshlaylik unda!",
    "ru": "Давайте начнем!"

}


select_channel = {
    "en": "Choose one of the channels:",
    "uz": "Kanallardan birini tanlang",
    "ru": "Выберите один из каналов"
}


no_channel = {
    "en": "Please add me to channel first",
    "uz": "Iltimos, avval meni kanalga qo'shing",
    "ru": "Пожалуйста, сначала добавьте меня в канал"
}


give_title = {
    "en": "Give a title for promo:",
    "uz": "Promo uchun nom bering",
    "ru": "Дайте название для промо"
}


choose_mode = {
    "en": "Choose the type\n\nmore info -> link", #TODO add link
    "uz": "Promo turini tanlang\n\nbatafsil ma'lumot -> havola",
    "ru": "Выберите тип\n\nподробнее -> ссылка"
}


choose_submode = {
    "en": "Choose the mode\n\nmore info -> link", #TODO add link
    "uz": "Rejimni tanlang\n\nbatafsil ma'lumot -> havola",
    "ru": "Выберите режим\n\nподробнее -> ссылка"
}


invite_numb = {
    "en": "Give the numbers of users participants should invite",
    "uz": "Ishtirokchilar taklif qilishi kerak bo'lgan foydalanuvchilar sonini kiriting",
    "ru": "Укажите количество пользователей, которых участники должны пригласить."
}


winners_numb = {
    "en": "Give the number of winners",
    "uz": "G'oliblar sonini kiriting",
    "ru": "Укажите количество победителей"
}


give_int = {
    "en": "Please provide integer number!",
    "uz": "Iltimos, butun son kiriting!",
    "ru": "Пожалуйста, укажите целое число!"
}


give_exp = {
    "en": "Give the expiry date and time in format dd.mm.yyyy hh:mm",
    "uz": "Tugash sanasi va vaqtini quyidagi formatda kiriting kun.oy.yil soat:daqiqa",
    "ru": "Укажите дату и время истечения срока действия в формате дд.мм.гггг чч:мм"
}


async def is_correct(usrlang, title, mode, exp, inv, winners):
    info = {
        "ref": {
            "en": f"Check if everything is correct\n\n*Title:* {title}\n*Mode:* Referral {mode.split('_')[1]}\n*Expires:* {exp}\n*Should invite (for random submode only):* {inv}\n\n*Number of winners:* {winners}",
            "uz": f"Hammasi to'g'ri ekanini tekshiring\n\n*Sarlavha:* {title}\n*Turi:* Referral {mode.split('_')[1]}\n*Tugash muddati:* {exp}\n*Taklif qilish kerak (faqat tasodifiy rejim uchun):* {inv}\n\n*G'oliblar soni:* {winners}",
            "ru": f"Проверьте, все ли правильно\n\n*Заголовок:* {title}\n*Тип:* Referral {mode.split('_')[1]}\n*Истекает:* {exp}\n*Нужно пригласить (только для рандом режима):* {inv}\n\n*Количество победителей:* {winners}"
        },
        "sub": {
            "en": f"Check if everything is correct\n\n*Title:* {title}\n*Mode:* Subscription {mode.split('_')[1]}\n*Expires:* {exp}\n\n*Number of winners:* {winners}",
            "uz": f"Hammasi to'g'ri ekanini tekshiring\n\n*Sarlavha:* {title}\n*Turi:* Subscription {mode.split('_')[1]}\n*Tugash muddati:* {exp}\n\n*G'oliblar soni:* {winners}",
            "ru": f"Проверьте, все ли правильно\n\n*Заголовок:* {title}\n*Тип:* Subscription {mode.split('_')[1]}\n*Истекает:* {exp}\n\n*Количество победителей:* {winners}"
        }
    }
    return info[mode.split('_')[0]][usrlang]


give_post = {
    "en": "Now send me your post that will be shared (published)",
    "uz": "Endi menga e’lon qilinadigan postingizni yuboring",
    "ru": "Теперь пришлите мне ваш пост, который будет опубликован"
}


published = {
    "en": "🚀 published to channel",
    "uz": "🚀 kanalda e'lon qilindi",
    "ru": "🚀 опубликовано на канале"
}


promo_exp = {
    "en": "The promo expired or does not exist",
    "uz": "Promo muddati tugagan yoki mavjud emas",
    "ru": "Срок действия промо-акции истек или она не существует"
}


sub_first = {
    "en": "Please subscribe to channel first. ",
    "uz": "Iltimos, avval kanalga obuna bo'ling. ",
    "ru": "Пожалуйста, сначала подпишитесь на канал. "
}


ur_reflink = {
    "en": "Here is your referral link (via which you can invite) ",
    "uz": "Mana sizning havolangiz (u orqali boshqalarni taklif qilishingiz mumkin) ",
    "ru": "Вот ваша реферальная ссылка (по которой вы можете пригласить) "
}


done_par = {
    "en": "✔️ Done you are participant",
    "uz": "✔️ Tayyor, siz ishtirokchisiz",
    "ru": "✔️ Готово, вы участник"
}


no_reflinks = {
    "en": "You do not have any active referral links",
    "uz": "Sizda faol havolalar yo'q",
    "ru": "У вас нет активных реферальных ссылок"
}


async def inv_info(usrlang, joined, link):
    res = {
        "en": f"People joined: {joined}\n\nReferкal link:\n{link}",
        "uz": f"Qo'shilganlar soni: {joined}\n\nReferral havola:\n{link}",
        "ru": f"Присоединились: {joined}\n\nРеферальная ссылка:\n{link}"
    }
    return res[usrlang]


async def no_winners(usrlang, promo, plcount, joincount):
    res = {
        "en": f"There is no winners on promo: {promo}\n\nParticipated: {plcount}\nNew joins: {joincount}",
        "uz": f"Quyidagi promoda g'oliblar yo'q: {promo}\n\nIshtirok etdi: {plcount}\nYangi qo'shildi: {joincount}",
        "ru": f"В следующем промо нет победителей: {promo}\n\nУчаствовали: {plcount}\nНовые подписчики: {joincount}"
    }
    return res[usrlang]


winners_an =  {
    "en": "🏆 winners_Check results 🔍",
    "uz": "🏆 g'oliblar_Natijalarni tekshirish 🔍",
    "ru": "🏆 победители_Проверить результаты 🔍"
}


link_to_promo = {
    "en": "✅ Done!\n\nLink to promo: ",
    "uz": "✅ Tayyor!\n\nPromoga havola: ",
    "ru": "✅ Готово!\n\nСсылка на промо: "
}


cpy_link = {
    "en": "Copy link",
    "uz": "Havolani nusxalash",
    "ru": "Скопировать ссылку" 
}