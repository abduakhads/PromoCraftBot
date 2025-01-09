import asyncio

from aiogram import Dispatcher, Bot, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import cfg
import keyboards as kb
from database import dbrequests
from handlers import change_lang, create_promo, add_channels, active_promos, defaultresp

dp = Dispatcher()
    

@dp.message(Command("start"))
async def startcmd(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Hi, welcome to our bot!", 
        reply_markup=types.reply_keyboard_remove.ReplyKeyboardRemove()
    )
    if not message.from_user.id in dbrequests.userslang:
        usr = [message.from_user.id, "en",
               message.from_user.full_name, str(message.from_user.username)] #edit! change table remove not bull
        dbrequests.create_user_db(*usr)
        await change_lang.set_lang(message, state)
        return
    await message.answer(
        "👋",
        reply_markup=await kb.get_main_kb(dbrequests.userslang[message.from_user.id])
    )


async def main() -> None:
    bot = Bot(token=cfg.BOT_TOKEN)
    dp.include_routers(
        add_channels.router,
        create_promo.router,
        active_promos.router,
        change_lang.router,
        defaultresp.router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, handle_signals=True)


@dp.startup()
async def start_bot():
    dbrequests.setup_tables_db()
    dbrequests.userslang = dbrequests.load_ulangs_db()
    print(dbrequests.userslang)
    print("Online")


@dp.shutdown()
async def stop_bot():
    dbrequests.close_all_db()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        start_bot()
