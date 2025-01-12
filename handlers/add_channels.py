import asyncio

from aiogram import Router, F, Bot, types
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER, BaseFilter


import lang
import keyboards as kb
from database import dbrequests
from handlers.my_activity import send_unotif

router = Router()


@router.message(F.text.in_(lang.my_channels.values()))
async def my_channels_show(message: types.Message):
    if res := dbrequests.load_uchannels_db(message.from_user.id):
        txt = "Here are your channels with me having correct rights\n\n"
        for row in res:
            txt += f"<a href='{row[2]}'>{row[1]}</a>\n"
        await message.answer(txt, parse_mode="html")
        return
    await message.answer(
            "You didn't add me to any channels", 
        )


@router.my_chat_member(ChatMemberUpdatedFilter(IS_MEMBER))
async def added_channel(update: types.ChatMemberUpdated, bot: Bot):
    await asyncio.sleep(1)
    try:
        link = f"t.me/{update.chat.username}" if (update.chat.username) else (await bot.get_chat(update.chat.id)).invite_link 
        if update.new_chat_member.can_post_messages and update.new_chat_member.can_invite_users:
            await bot.send_message(
                update.from_user.id, 
                f"added channel <a href='{link}'>{update.chat.title}</a>",parse_mode="html"
            )
            dbrequests.insert_channel_db(update.chat.id, update.from_user.id, update.chat.title, link)
            return
        await bot.send_message(
            update.from_user.id, 
            f"please give the admin rights mentioned in guide in channel: <a href='{link}'>{update.chat.title}</a>,\
            \n\notherwise bot can't publish results or add users to channel", parse_mode="html"
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
            f"bot was kicked from <a href='{dbrequests.get_channel_link_db(update.chat.id)[0][0]}'>{update.chat.title}</a>,\
                \nyour promos related to channel are deleted",
            parse_mode="html"
        )
        #TODO delete all promos
    except Exception as e:
        print(e)
    dbrequests.remove_channel_db(update.chat.id)



class ChatFilter(BaseFilter):
    async def __call__(self, update: types.ChatMemberUpdated):
        # print(update.invite_link)
        return True if update.invite_link else False


@router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER), ChatFilter())
async def joined_channel(update: types.ChatMemberUpdated):
    upd = update.invite_link.name.split(" ")
    reflinkid = dbrequests.update_reflink_join(upd[0], upd[1])[0]
    dbrequests.insert_join(reflinkid, update.from_user.id, update.chat.id)
    await send_unotif(upd[0], f"<a href='{update.from_user.username}'>{update.from_user.full_name}</a> joined via your <a href='{update.invite_link.invite_link}'>link</a>")


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER))
async def joined_channel(update: types.ChatMemberUpdated, bot: Bot):
    res = dbrequests.del_player(update.from_user.id, update.chat.id)
    # if res:
    #     for row in res:
    #         await bot.revoke_chat_invite_link(update.chat.id, row[0])
    if uid := dbrequests.del_join(update.from_user.id, update.chat.id):
        await send_unotif(uid[0], f"<a href='https://t.me/{update.from_user.username}'>{update.from_user.full_name}</a> left channel <a href='{(await bot.get_chat(update.chat.id)).invite_link}'> {update.chat.title}</a>")


@router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER))
async def joined_channel2(update: types.ChatMemberUpdated):
    dbrequests.joined_back(update.from_user.id, update.chat.id)