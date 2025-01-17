import asyncio

from aiogram import Router, F, Bot, types
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER, BaseFilter


import lang
from database import dbrequests
from handlers.my_activity import send_unotif
from bot import notify_players

router = Router()


@router.message(F.text.in_(lang.my_channels.values()))
async def my_channels_show(message: types.Message):
    if res := dbrequests.load_uchannels_db(message.from_user.id):
        txt = lang.on_channels[dbrequests.userslang[message.from_user.id]]
        for row in res:
            txt += f"<a href='{row[2]}'>{row[1]}</a>\n"
        await message.answer(txt, parse_mode="html")
        return
    await message.answer(
            lang.no_channels[dbrequests.userslang[message.from_user.id]]
        )


@router.my_chat_member(ChatMemberUpdatedFilter(IS_MEMBER))
async def added_channel(update: types.ChatMemberUpdated, bot: Bot):
    await asyncio.sleep(1)
    try:
        link = f"t.me/{update.chat.username}" if (update.chat.username) else (await bot.get_chat(update.chat.id)).invite_link 
        if update.new_chat_member.can_post_messages and update.new_chat_member.can_invite_users:
            await bot.send_message(
                update.from_user.id, 
                lang.added_channel[dbrequests.userslang[update.from_user.id]] + f"<a href='{link}'>{update.chat.title}</a>",parse_mode="html"
            )
            dbrequests.insert_channel_db(update.chat.id, update.from_user.id, update.chat.title, link)
            return
        await bot.send_message(
            update.from_user.id, 
            await lang.edited_ch_from(dbrequests.userslang[update.from_user.id], update.chat.title, link), 
            parse_mode="Markdown"
        )
        dbrequests.remove_channel_db(update.chat.id)
    except Exception as e:
        print(e)


@router.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER))
async def kicked_channel(update: types.ChatMemberUpdated, bot: Bot):
    await asyncio.sleep(1)
    try:
        await bot.send_message(
            dbrequests.get_usrby_channel_db(update.chat.id)[0][0], #error: list index out of range(when bot kicked and data no)
            await lang.kicked_from_ch(dbrequests.userslang[update.from_user.id], update.chat.title, dbrequests.get_channel_link_db(update.chat.id)[0][0]),
            parse_mode="Markdown"
        )
        #TODO delete all promos
    except Exception as e:
        print(e)
    dbrequests.remove_channel_db(update.chat.id)
    if uids := dbrequests.remove_all_kicked(update.chat.id):
        await notify_players(uids, update.chat.title)


class ChatFilter(BaseFilter):
    async def __call__(self, update: types.ChatMemberUpdated):
        # print(update.invite_link)
        return True if update.invite_link else False


@router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER), ChatFilter())
async def joined_channel(update: types.ChatMemberUpdated):
    if (upd := update.invite_link.name):
        upd = upd.split(" ")
        reflinkid = dbrequests.update_reflink_join(upd[0], upd[1])[0]
        dbrequests.insert_join(reflinkid, update.from_user.id, update.chat.id)
        await send_unotif(upd[0], f"<a href='{update.from_user.username}'>{update.from_user.full_name}</a> joined via your <a href='{update.invite_link.invite_link}'>link</a>")


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER))
async def left_channel(update: types.ChatMemberUpdated, bot: Bot):
    res = dbrequests.del_player(update.from_user.id, update.chat.id)
    # if res:
    #     for row in res:
    #         await bot.revoke_chat_invite_link(update.chat.id, row[0])
    if uid := dbrequests.del_join(update.from_user.id, update.chat.id):
        await send_unotif(uid[0], f"<a href='https://t.me/{update.from_user.username}'>{update.from_user.full_name}</a> left channel <a href='{(await bot.get_chat(update.chat.id)).invite_link}'> {update.chat.title}</a>")


@router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER))
async def joined_channel2(update: types.ChatMemberUpdated):
    dbrequests.joined_back(update.from_user.id, update.chat.id)