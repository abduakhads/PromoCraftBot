import asyncio

from aiogram import Dispatcher, Bot, types, F
from aiogram.filters import Command

import cfg, handlers, database
import handlers.change_lang
import handlers.create_promo


dp = Dispatcher()
    

@dp.message(Command("start"))
async def startcmd(message: types.Message):
    await message.answer(
        text="Hi, welcome to our bot!", 
        reply_markup=types.reply_keyboard_remove.ReplyKeyboardRemove()
    )
    if not message.from_user.id in database.dbrequests.userslang:
        usr = [message.from_user.id, str(None),
               message.from_user.full_name, str(message.from_user.username)]
        database.dbrequests.create_user_db(*usr)
        await handlers.change_lang.set_lang(message)


async def main() -> None:
    bot = Bot(token=cfg.BOT_TOKEN)
    dp.include_routers(
        handlers.change_lang.router, 
        handlers.create_promo.router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, handle_signals=True)


@dp.startup()
async def start_bot(bot: Bot):
    database.dbrequests.setup_tables_db()
    database.dbrequests.userslang = database.dbrequests.load_ulangs_db()
    print(database.dbrequests.userslang)
    print("Online")


@dp.shutdown()
async def stop_bot():
    database.dbrequests.close_all_db()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        stop_bot()