from aiogram import Router, F, types

import lang, cfg
import keyboards as kb
from database import dbrequests


router = Router()


@router.message(F.text.in_(lang.my_promos.values()))
async def my_promos_show(message: types.Message):
    if not (inkb := await kb.get_upromos_inkb(message.from_user.id)):
        await message.answer(lang.no_promos[dbrequests.userslang[message.from_user.id]])
        return
    await message.answer(
            lang.on_promos[dbrequests.userslang[message.from_user.id]],
            reply_markup=inkb
        )
    
@router.callback_query(F.data.startswith('forpromo'))
async def show_promo_stats(callback: types.CallbackQuery):
    promo = dbrequests.get_promo(int(callback.data.split("_")[1]))
    plcount = dbrequests.get_participants_count(int(callback.data.split('_')[1]), promo[1].split("_")[0])[0]
    joincount = dbrequests.get_joins_count(int(callback.data.split('_')[1]))[0]
    usrlang = dbrequests.userslang[callback.from_user.id]
    await callback.message.edit_text(
        await lang.promo_info(usrlang, callback.data.split('_')[1], promo[1], promo[2], promo[3], plcount, joincount, promo[4], promo[5]),
        parse_mode="Markdown",
        reply_markup=await kb.get_copy_inkb(
            text=lang.cpy_link[usrlang],
            cpy=f"t.me/{cfg.UBOT_USERNANE}?start=promo_{callback.data.split('_')[1]}"
        )
    )
    await callback.answer()