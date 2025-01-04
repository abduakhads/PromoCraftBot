import asyncio

from aiogram import Router, F, Bot, types
from aiogram.filters import Command, ChatMemberUpdatedFilter, PROMOTED_TRANSITION


router = Router()


# @router.message(Command("revoke"))
# async def getId(message: types.Message, bot: Bot):
    # await bot.send_message(chat_id=cfg.CHANNEL_ID, text=mention, parse_mode="Markdown")
    # await bot.revoke_chat_invite_link(cfg.CHANNEL_ID, "https://t.me/+i77Rc3DLgj4wYjBi")
    # await message.answer("done")


@router.my_chat_member(ChatMemberUpdatedFilter(PROMOTED_TRANSITION))
async def statuses(update: types.ChatMemberUpdated, bot: Bot):
    await asyncio.sleep(0.8)
    link = (await bot.get_chat(update.chat.id)).invite_link
    await bot.send_message(
        update.from_user.id, 
        f"joined to <a href='{link}'>{update.chat.title}</a>",parse_mode="html"
    )
    #TODO save channel id
    await bot.send_message(update.chat.id, "im admin")
    # await bot.get
    # link = await bot.create_chat_invite_link(cfg.CHANNEL_ID, f"Invitation for {update.from_user.full_name}", member_limit=1)
    # await bot.send_message(update.from_user.id,link.invite_link)