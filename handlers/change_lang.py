from aiogram import Router, F, types

import lang
import keyboards as kb
from database import dbrequests


router = Router()


@router.message(F.text.in_(lang.change_lang.values()))
async def set_lang(message: types.Message):
    await message.answer(
        text="Please choose language:",
        reply_markup=await kb.get_lang_inkb()
    )


@router.callback_query(F.data.startswith("set"))
async def set_lang_call(callback: types.CallbackQuery):
    dbrequests.userslang[callback.from_user.id] = callback.data.split("_")[1]
    dbrequests.upd_ulang_db(callback.from_user.id, dbrequests.userslang[callback.from_user.id])
    print(dbrequests.userslang)
    await callback.message.delete()
    await callback.message.answer(
        text=lang.set_lang_done[dbrequests.userslang[callback.from_user.id]],
        reply_markup=await kb.get_main_kb(dbrequests.userslang[callback.from_user.id])
    )
    await callback.answer()