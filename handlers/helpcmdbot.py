from aiogram import Router, types, F
from aiogram.filters import Command

import lang
from database import dbrequests
import keyboards as kb


router = Router()


@router.callback_query(F.data.startswith("done_read"))
async def done_read_docs(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        text=lang.need_help[dbrequests.userslang[callback.from_user.id]],
        reply_markup=await kb.get_main_kb(dbrequests.userslang[callback.from_user.id])
    )
    await callback.answer()


@router.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer(
        text=lang.help_cmd[dbrequests.userslang[message.from_user.id]],
        parse_mode="Markdown"
    )
    
