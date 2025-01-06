import asyncio

from aiogram import Router, F, Bot, types
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER

import lang
import keyboards as kb
from database import dbrequests


router = Router()


@router.message(F.text.in_(lang.my_promos.values()))
async def my_promos_show(message: types.Message):
    await message.answer(
            "Here your active promos",
            reply_markup=await kb.get_upromos_inkb(message.from_user.id)
        )
    
@router.callback_query(F.data.startswith('forpromo'))
async def show_promo_stats(callback: types.CallbackQuery):
    await callback.message.edit_text("here your stats")
    await callback.answer()