import asyncio

from aiogram import Dispatcher, Bot, types, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime

import cfg, lang
import keyboards as kb
from database import dbrequests
from handlers import change_lang, create_promo, add_channels, active_promos, defaultresp, my_activity, helpcmdbot

dp = Dispatcher()
upd = Dispatcher()
bot = Bot(token=cfg.BOT_TOKEN)
ubot = Bot(token=cfg.UBOT_TOKEN)


class TakePart(StatesGroup):
    register = State()


@dp.message(Command("start"))
async def startcmd(message: types.Message, state: FSMContext):
    await state.clear()
    if not message.from_user.id in dbrequests.userslang:
        usr = [message.from_user.id, "en",
               message.from_user.full_name, str(message.from_user.username)] #edit! change table remove not bull
        dbrequests.create_user_db(*usr)
        await change_lang.set_lang(message, state, is_start = True)
        return
    await message.answer(
        "👋",
        reply_markup=await kb.get_main_kb(dbrequests.userslang[message.from_user.id])
    )


@upd.message(Command("start"))
async def ustartcmd(message: types.Message, command: CommandObject, state: FSMContext):
    if command.args and command.args.split("_")[0] == "promo":
        if message.from_user.id in dbrequests.userslang:
            await my_activity.register_part(message.from_user.id, command.args.split("_")[1])
            return
        await state.set_state(TakePart.register)
        await state.update_data(promo_id=command.args.split("_")[1])
    elif command.args and command.args.split("_")[0] == "check":
        if text := dbrequests.check_winners(command.args.split("_")[1]):
            if text[0]:
                await ubot.copy_message(message.chat.id, cfg.WINNER_LOG_CHANNEL, text[0])
                return
    if not message.from_user.id in dbrequests.userslang:
        usr = [message.from_user.id, "en",
                message.from_user.full_name, str(message.from_user.username)] #edit! change table remove not bull
        dbrequests.create_user_db(*usr)
        await my_activity.set_ulang(message)
        return 
    await message.answer("👋", reply_markup=await kb.get_main_kb(dbrequests.userslang[message.from_user.id], True))


async def process_promos():
    tasks = dbrequests.get_ready_promos(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for task in tasks:
        # print(task)
        if not (winnersids := dbrequests.get_players(task[0], task[7], task[5], task[3].split("_")[0])):
            if task[3].split("_")[0] == "ref":
                revokeln = dbrequests.get_reflinks_torevoke(task[0])
                await revoke_links(task[2], revokeln)
                joincount = dbrequests.get_joins_count(task[0], delete=True)[0]
            elif task[3].split("_")[0] == "sub":
                joincount = "-"
            plcount = dbrequests.get_participants_count(task[0], task[3].split("_")[0], delete=True)[0]
            await bot.send_message(task[1], await lang.no_winners(dbrequests.userslang[task[1]], task[4], plcount, joincount))
            continue
        wintxt = lang.winners_an[dbrequests.userslang[task[1]]].split("_")
        if task[3].split("_")[0] == "ref":
            if task[3].split("_")[1] == "random":
                winners = dbrequests.get_users(winnersids)
                mentions = [types.User(id=row[0], is_bot=False, first_name=row[2]).mention_markdown(name=row[2]) for row in winners]
                text = f"{wintxt[0]}: \n\n" + '\n'.join(f"{index + 1}. {mention}" for index, mention in enumerate(mentions))
            elif task[3].split("_")[1] == "most":
                winners = dbrequests.get_users(winnersids.keys())
                winners = sorted(winners, key=lambda x: list(winnersids.keys()).index(x[0]))
                # ids = [row[0] for row in winners]
                topjoins = list(winnersids.values())
                mentions = [types.User(id=row[0], is_bot=False, first_name=row[2]).mention_markdown(name=row[2]) for row in winners]
                text = f"{wintxt[0]}: \n\n" + '\n'.join(f"{index + 1}. {mention} {topjoins[index]}" for index, mention in enumerate(mentions))
            revokeln = dbrequests.get_reflinks_torevoke(task[0])
            await revoke_links(task[2], revokeln)
            joincount = dbrequests.get_joins_count(task[0], delete=True)[0]
        elif task[3].split("_")[0] == "sub":
            winners = dbrequests.get_users(winnersids)
            mentions = [types.User(id=row[0], is_bot=False, first_name=row[2]).mention_markdown(name=row[2]) for row in winners]
            text = f"{wintxt[0]}: \n\n" + '\n'.join(f"{index + 1}. {mention}" for index, mention in enumerate(mentions))
            joincount = "-"
        plcount = dbrequests.get_participants_count(task[0], task[3].split("_")[0], delete=True)[0]
        # forlog = "promoId: " + str(task[0]) + "\npromo mode: " + task[3].replace('_', " ").title() + "\npromo title: " + task[4] + "\nend date: " + str(task[6]) + "\nwinners count: " + str(task[5]) + "\nparticipants: " + str(plcount) + "\nnew subs: " + str(joincount) + "\n\n" + text
        forlog = await lang.promo_info(dbrequests.userslang[task[1]], task[0], task[3], task[6], task[7], plcount, joincount, task[4], task[5]) + "\n\n" + text + f"\n\n[{wintxt[1]}](https://t.me/{cfg.UBOT_USERNANE}?start=check_{task[0]})"
        mess_id = (await ubot.send_message(cfg.WINNER_LOG_CHANNEL, forlog, parse_mode="Markdown", link_preview_options=types.LinkPreviewOptions(is_disabled=True))).message_id
        if task[9]:
            replyid = int(task[9]) * (-1)
        else:
            replyid = None
        dbrequests.save_winners(task[0], mess_id)
        if replyid:
            await bot.send_message(task[2], text, parse_mode="Markdown", reply_markup=await kb.get_link_inkb(wintxt[1], f"https://t.me/{cfg.UBOT_USERNANE}?start=check_{task[0]}"), link_preview_options=None, reply_to_message_id=replyid)
        else:
            await bot.send_message(task[2], text, parse_mode="Markdown", reply_markup=await kb.get_link_inkb(wintxt[1], f"https://t.me/{cfg.UBOT_USERNANE}?start=check_{task[0]}"), link_preview_options=None)


async def revoke_links(channel_id: int, links: list):
    for row in links:
        await bot.revoke_chat_invite_link(channel_id, row[0])


async def notify_players(uids: list, title: str):
    for uid in uids:
        await ubot.send_message(uid, lang.promo_canceled[dbrequests.userslang[uid]] + title)


async def run_periodic_tasks():
    while True:
        await process_promos()
        await asyncio.sleep(10)
    

async def main() -> None:
    asyncio.create_task(run_periodic_tasks())

    dp.include_routers(
        add_channels.router,
        create_promo.router,
        active_promos.router,
        change_lang.router,
        helpcmdbot.router,
        defaultresp.router,
    )
    upd.include_routers(my_activity.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await ubot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(
        upd.start_polling(ubot, handle_signals=True),
        dp.start_polling(bot, handle_signals=True),
    )


@dp.startup()
async def start_bot():
    # dbrequests.setup_tables_db()
    dbrequests.userslang = dbrequests.load_ulangs_db()
    # print(dbrequests.userslang)
    print("Online")


@dp.shutdown()
def stop_bot():
    dbrequests.close_all_db()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        stop_bot()
