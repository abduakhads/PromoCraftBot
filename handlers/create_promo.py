from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import lang, cfg
from handlers.helpfuncs import is_valid_datetime
import keyboards as kb
from database import dbrequests
from handlers.middlwares import CancellForAll
from handlers.change_lang import set_timediff


router = Router()
router.message.middleware(CancellForAll())

class CreatePromo(StatesGroup):
    channel_id = State()
    title = State()
    mode = State()
    confmod = State()
    memberlimit = State()
    winner_count = State()
    expiration = State()
    confirm = State()
    post = State()


@router.message(F.text.in_(lang.init_promo.values()))
async def create_promo_0(message: types.Message, state: FSMContext):
    if not dbrequests.get_utimdiff_db(message.from_user.id)[0][0]:
        await message.answer(lang.need_conf_tim[dbrequests.userslang[message.from_user.id]])
        await set_timediff(message, state)
        return
    if dbrequests.load_uchannels_db(message.from_user.id):
        await message.answer(
            text=lang.lets_start[dbrequests.userslang[message.from_user.id]],
            reply_markup=await kb.cancel_all_kb(dbrequests.userslang[message.from_user.id])
        )
        await message.answer(
            text=lang.select_channel[dbrequests.userslang[message.from_user.id]],
            reply_markup=await kb.get_uchannels_inkb(message.from_user.id),
        )
        await state.set_state(CreatePromo.channel_id)
        return
    await message.answer(
            text=lang.no_channel[dbrequests.userslang[message.from_user.id]]
        )


@router.message(CreatePromo.channel_id)
async def create_promo_1can(message: types.Message):
    pass

@router.callback_query(CreatePromo.channel_id, F.data.startswith('forchan'))#####
async def create_promo_1(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(channel_id=callback.data.split("_")[1])
    await callback.message.edit_text(
        f"✔️ <a href='{callback.data.split('_')[2]}'>{dbrequests.get_channel_link_db(callback.data.split('_')[1])[0][1]}</a>",
        parse_mode="html"
    )
    await callback.message.answer(
        text=lang.give_title[dbrequests.userslang[callback.from_user.id]]
    )
    await state.set_state(CreatePromo.title)
    await callback.answer()


@router.message(CreatePromo.title)
async def create_promo_2(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer(
        text=lang.choose_mode[dbrequests.userslang[message.from_user.id]],
        reply_markup=await kb.get_prmodes_inkb()
    )
    await state.set_state(CreatePromo.mode)


@router.message(CreatePromo.mode)
async def create_promo_3can(message: types.Message):
    pass


@router.callback_query(CreatePromo.mode, F.data.startswith('mode'))
async def create_promo_3(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(mode=callback.data.split("_")[1])
    await callback.message.edit_text(f"✔️ {callback.data.split('_')[1]}")
    await callback.message.answer(
        text=lang.choose_submode[dbrequests.userslang[callback.from_user.id]],
        reply_markup=await kb.get_prconfmodes_inkb(await state.get_value("mode"))
    )
    await state.set_state(CreatePromo.confmod)
    await callback.answer()


@router.message(CreatePromo.confmod)
async def create_promo_4can(message: types.Message):
    pass

@router.callback_query(CreatePromo.confmod, F.data.startswith('confmode'))
async def create_promo_4(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(confmod=callback.data.split("_")[1])
    await callback.message.edit_text(f"✔️ {callback.data.split('_')[1]}")
    if callback.data.split("_")[1] == "random" and (await state.get_value("mode")) == "ref":
        await callback.message.answer(
            text=lang.invite_numb[dbrequests.userslang[callback.from_user.id]],
        )
        await state.set_state(CreatePromo.memberlimit)
        await callback.answer()
        return
    await callback.message.answer(
        text=lang.winners_numb[dbrequests.userslang[callback.from_user.id]]
    )
    await state.set_state(CreatePromo.winner_count)
    await callback.answer()


@router.message(CreatePromo.memberlimit)
async def create_promo_45(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.reply(text=lang.give_int[dbrequests.userslang[message.from_user.id]])
        return
    await state.update_data(memberlimit=message.text)
    await message.answer(
        text=lang.winners_numb[dbrequests.userslang[message.from_user.id]]
    )
    await state.set_state(CreatePromo.winner_count)


@router.message(CreatePromo.winner_count)
async def create_promo_5(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.reply(text=lang.give_int[dbrequests.userslang[message.from_user.id]])
        return
    await state.update_data(winner_count=message.text)
    await message.answer(
        text=lang.give_exp[dbrequests.userslang[message.from_user.id]]
    )
    await state.set_state(CreatePromo.expiration)


@router.message(CreatePromo.expiration)
async def create_promo_6(message: types.Message, state: FSMContext):
    if not (expdt := is_valid_datetime(message.text, dbrequests.get_utimdiff_db(message.from_user.id)[0][0].split(":"))):
        await message.answer(text=lang.give_exp[dbrequests.userslang[message.from_user.id]])
        return
    await state.update_data(expiration=expdt)
    data = await state.get_data()
    text = await lang.is_correct(dbrequests.userslang[message.from_user.id], data['title'], f"{data['mode']}_{data['confmod']}", data['expiration'] ,await state.get_value('memberlimit'), data['winner_count'])
    # text = "Please check if everything is correct\n\n" + f"Title: {data['title']}\nMode: {data['mode']} {data['confmod']}\nShould invite(for ref random mode only): {await state.get_value('memberlimit')}\nWinner count: {data['winner_count']}\nDate: {data['expiration']}" 
    await message.answer(
        text=text,
        reply_markup=await kb.get_confirm_inkb(dbrequests.userslang[message.from_user.id]),
        parse_mode="Markdown"
    )
    await state.set_state(CreatePromo.confirm)


@router.message(CreatePromo.confirm)
async def create_promo_7can(message: types.Message):
    pass

@router.callback_query(CreatePromo.confirm, F.data.startswith('confirm'))
async def create_promo_7(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("✔️")
    await callback.message.answer(
        text=lang.give_post[dbrequests.userslang[callback.from_user.id]]
    )
    await state.set_state(CreatePromo.post)
    await callback.answer()


@router.message(CreatePromo.post)
async def create_promo_8(message: types.Message, state: FSMContext):
    data = await state.get_data()
    promo_id = dbrequests.save_promo_db(
        message.from_user.id, data['channel_id'], f"{data['mode']}_{data['confmod']}",
        data['title'], data['winner_count'], data['expiration'], await state.get_value("memberlimit")
    )
    
    promo_link = "t.me/" + cfg.UBOT_USERNANE + "?start=promo_" + str(promo_id)
    await message.copy_to(
        message.from_user.id, 
        reply_markup=await kb.get_postready_inkb(
            dbrequests.userslang[message.from_user.id],
            promo_link,
            data["channel_id"],
            promo_id
        )
    )
    await message.answer(
        lang.link_to_promo[dbrequests.userslang[message.from_user.id]], 
        reply_markup=await kb.get_main_kb(dbrequests.userslang[message.from_user.id])
    )
    await message.answer(
        promo_link, 
        reply_markup=await kb.get_copy_inkb(
            text=lang.cpy_link[dbrequests.userslang[message.from_user.id]],
            cpy=promo_link
        ),
        link_preview_options=types.LinkPreviewOptions(is_disabled=True)
    )
    await state.clear()


@router.callback_query(F.data.startswith('publish_promo'))
async def publish_promo(callback: types.CallbackQuery):
    await callback.message.copy_to(
        callback.data.split("_")[2], 
        reply_markup=await kb.get_link_inkb(
            lang.takepart[dbrequests.userslang[callback.from_user.id]],
            "_".join(callback.data.split("_")[3:])
        )
    )
    await callback.answer(
        text=lang.published[dbrequests.userslang[callback.from_user.id]]
    )


    # link = await bot.create_chat_invite_link(cfg.CHANNEL_ID, f"Invitation for {update.from_user.full_name}", member_limit=1)
    # await bot.send_message(update.from_user.id,link.invite_link)

# @router.message(Command("revoke"))
# async def revoke_link(message: types.Message, bot: Bot):
    # await bot.send_message(chat_id=cfg.CHANNEL_ID, text=mention, parse_mode="Markdown")
    # await bot.revoke_chat_invite_link(cfg.CHANNEL_ID, "https://t.me/+i77Rc3DLgj4wYjBi")
    # await message.answer("done")


# async def cancel_forall(message: types.Message, state: FSMContext):
#     await state.clear()
#     await message.answer(
#         lang.cancel_done(dbrequests.userslang[message.from_user.id]),
#         reply_markup=await kb.get_main_kb(dbrequests.userslang[message.from_user.id])
#     )
