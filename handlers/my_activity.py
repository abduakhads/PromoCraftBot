from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from datetime import datetime

from bot import TakePart
import lang, bot
import keyboards as kb
from database import dbrequests
from aiogram.filters import BaseFilter

class ChatFilter(BaseFilter):
    async def __call__(self, update: types.ChatMemberUpdated):
        return True if update.invite_link else False

router = Router()


@router.message(F.text.in_(lang.change_lang.values()))
async def set_ulang(message: types.Message):
   
   await message.answer(
        text="Please choose language:",
        reply_markup=await kb.get_lang_inkb()
    )

@router.callback_query(F.data.startswith("set"), (TakePart.register))
async def set_ulang_call(callback: types.CallbackQuery, state: FSMContext):
    dbrequests.userslang[callback.from_user.id] = callback.data.split("_")[1]
    dbrequests.upd_ulang_db(callback.from_user.id, dbrequests.userslang[callback.from_user.id])
    await callback.message.delete()
    await callback.message.answer(
        text=lang.set_lang_done[dbrequests.userslang[callback.from_user.id]],
        reply_markup=await kb.get_main_kb(dbrequests.userslang[callback.from_user.id], player=True)
    )
    if str(await state.get_state()) == "TakePart:register":
        await register_part(callback.from_user.id, await state.get_value("promo_id"))
        await state.clear()
    await callback.answer()


async def register_part(user_id, promo_id):
    if not (res := dbrequests.get_promo(promo_id)):
        await bot.ubot.send_message(user_id, "The promo expired or does not exist")
        return
    if (await bot.bot.get_chat_member(res[0], user_id)).status == "left":
        invlink = (await bot.bot.get_chat(res[0])).invite_link
        await bot.ubot.send_message(user_id, f"please subscribe to <a href='{invlink}'>channel</a> first", parse_mode="html")
        return
    if res[1].startswith("ref"):
        if promo := dbrequests.get_reflink(user_id, promo_id):
            await bot.ubot.send_message(user_id, f"hereis your link {promo[1]}")
            return
        chatlink = await bot.bot.create_chat_invite_link(
            res[0], f"{user_id} {promo_id}", datetime.strptime(res[2], '%Y-%m-%d %H:%M:%S'), res[3]
        )
        dbrequests.set_reflink(user_id, promo_id, chatlink.invite_link)
        await bot.ubot.send_message(user_id, f"here is your ref link {chatlink.invite_link}")
    elif res[1].startswith("sub"):
        if not dbrequests.get_sub(user_id, promo_id):
            dbrequests.insert_sub(user_id, promo_id)
        await bot.ubot.send_message(user_id, f"done you are participant")


@router.callback_query(F.data.startswith("set"))
async def set_ulang_call2(callback: types.CallbackQuery, state: FSMContext):
    await set_ulang_call(callback, state)


async def send_unotif(user_id: int, text: str):
    await bot.ubot.send_message(user_id, text, parse_mode="html")


@router.message(F.text.in_(lang.my_links.values()))
async def show_links(message: types.Message):
    if not (inkb := (await kb.get_urelfliks_inkb(message.from_user.id))):
        await message.answer("you don't have any active referal links")
        return
    await message.answer("choose promo", reply_markup=inkb)


@router.callback_query(F.data.startswith("forreflink"))
async def show_links_call(callback: types.CallbackQuery):
    await callback.message.edit_text(
        f"People joined: {callback.data.split('_')[1]}\n\nLink: {'_'.join(callback.data.split('_')[2:])}",
        # reply_markup=await kb.get_copy_inkb('_'.join(callback.data.split('_')[2:]))
    )
    await callback.answer()