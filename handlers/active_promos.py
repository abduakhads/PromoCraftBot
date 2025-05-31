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
    if not dbrequests.is_promo_active(int(callback.data.split("_")[1])):
        await callback.message.edit_text(lang.promo_finished[dbrequests.userslang[callback.from_user.id]])
        await callback.answer()
        return
    promo = dbrequests.get_promo(int(callback.data.split("_")[1]))
    plcount = dbrequests.get_participants_count(int(callback.data.split('_')[1]), promo[1].split("_")[0])[0]
    joincount = dbrequests.get_joins_count(int(callback.data.split('_')[1]))[0]
    usrlang = dbrequests.userslang[callback.from_user.id]
    await callback.message.edit_text(
        await lang.promo_info(usrlang, callback.data.split('_')[1], promo[1], promo[2], promo[3], plcount, joincount, promo[4], promo[5]),
        parse_mode="Markdown",
        reply_markup=await kb.promos_inkb(
            dbrequests.userslang[callback.from_user.id],
            callback.data.split('_')[1],
            text=lang.cpy_link[usrlang],
            cpy=f"t.me/{cfg.UBOT_USERNANE}?start=promo_{callback.data.split('_')[1]}"
        )
    )
    await callback.answer()


@router.callback_query(F.data.startswith('cancel_promo'))
async def cancel_promo(callback: types.CallbackQuery):
    if not dbrequests.is_promo_active(int(callback.data.split("_")[2])):
        await callback.message.edit_text(lang.promo_finished[dbrequests.userslang[callback.from_user.id]])
        await callback.answer()
        return
    await callback.message.edit_text(
        lang.cancel_promo_inkb[dbrequests.userslang[callback.from_user.id]] + "?",
        reply_markup=await kb.confirm_inkb(
            dbrequests.userslang[callback.from_user.id],
            callback.data.split('_')[2],
            type='cancel' 
        )
    )
    await callback.answer()


@router.callback_query(F.data.startswith('confirm_promo_cancel'))
async def confirm_cancel_promo(callback: types.CallbackQuery):
    promo_id = int(callback.data.split('_')[3])
    if not dbrequests.is_promo_active(promo_id):
        await callback.message.edit_text(lang.promo_finished[dbrequests.userslang[callback.from_user.id]])
        await callback.answer()
        return
    from bot import revoke_links, notify_players
    uids, links, channel_id, channel_name = dbrequests.cancel_promo_db(promo_id)
    await revoke_links(channel_id, [[row] for row in links])
    await notify_players(uids, channel_name)
    await callback.message.edit_text(lang.cancel_done[dbrequests.userslang[callback.from_user.id]])
    await callback.answer()


@router.callback_query(F.data.startswith('finish_promo'))
async def finish_promo(callback: types.CallbackQuery):
    if not dbrequests.is_promo_active(int(callback.data.split("_")[2])):
        await callback.message.edit_text(lang.promo_finished[dbrequests.userslang[callback.from_user.id]])
        await callback.answer()
        return
    await callback.message.edit_text(
        lang.finish_promo_inkb[dbrequests.userslang[callback.from_user.id]] + "?",
        reply_markup=await kb.confirm_inkb(
            dbrequests.userslang[callback.from_user.id],
            callback.data.split('_')[2],
            type='finish'
        )
    )


@router.callback_query(F.data.startswith('confirm_promo_finish'))
async def confirm_finish_promo(callback: types.CallbackQuery):
    if not dbrequests.is_promo_active(int(callback.data.split("_")[3])):
        await callback.message.edit_text(lang.promo_finished[dbrequests.userslang[callback.from_user.id]])
        await callback.answer()
        return
    promo_id = int(callback.data.split('_')[3])
    dbrequests.finish_promo_db(promo_id)
    await callback.message.edit_text(
        text=lang.promo_finished[dbrequests.userslang[callback.from_user.id]]
    )

