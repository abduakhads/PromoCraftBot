import cfg
import asyncio

from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command
import pprint

dp = Dispatcher()


@dp.message(Command('getlink'))
async def getId(message: types.Message, bot: Bot):
    # await bot.send_message(message.chat.id, str(message.forward_from_chat.id))
    link = await bot.create_chat_invite_link(cfg.CHANNEL_ID, f"Invitation for {message.from_user.full_name}", member_limit=1)
    # await message.answer(str(link))
    await message.answer(link.invite_link)

async def main() -> None:
    bot = Bot(token=cfg.BOT_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, handle_signals=True)

@dp.startup()
async def start():
    print("Online")

if __name__ == "__main__":
    asyncio.run(main())
