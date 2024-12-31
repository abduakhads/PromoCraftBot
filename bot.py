import cfg
import asyncio

from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command, ChatMemberUpdatedFilter, PROMOTED_TRANSITION


dp = Dispatcher()


@dp.my_chat_member(ChatMemberUpdatedFilter(PROMOTED_TRANSITION))
async def statuses(update: types.ChatMemberUpdated, bot: Bot):
    await asyncio.sleep(1)

    link = (await bot.get_chat(update.chat.id)).invite_link
    await bot.send_message(
        update.from_user.id, 
        f"joined to <a href='{link}'>{update.chat.title}</a>",parse_mode="html"
    )
    #TODO save channel id
    await bot.send_message(update.chat.id, "im admin")
    

# @dp.message()
# async def getId(message: types.Message, bot: Bot):
#     link = await bot.create_chat_invite_link(cfg.CHANNEL_ID, f"Invitation for {message.from_user.full_name}", member_limit=1)
#     await message.answer(link.invite_link)


async def main() -> None:
    bot = Bot(token=cfg.BOT_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, handle_signals=True)


@dp.startup()
async def start(bot: Bot):
    print("Online")


if __name__ == "__main__":
    asyncio.run(main())
