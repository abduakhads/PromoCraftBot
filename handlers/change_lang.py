from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import lang
import keyboards as kb
from database import dbrequests
from handlers.helpfuncs import get_time_difference
from handlers.middlwares import CancellForAll

router = Router()
router.message.middleware(CancellForAll())

class TimeDiffSet(StatesGroup):
    utimediff = State()


@router.message(F.text.in_(lang.change_lang.values()))
async def set_lang(message: types.Message, state: FSMContext):
    if (await state.get_state()):
        return
    await message.answer(
        text="Please choose language:",
        reply_markup=await kb.get_lang_inkb()
    )


@router.callback_query(F.data.startswith("set"))
async def set_lang_call(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    dbrequests.userslang[callback.from_user.id] = callback.data.split("_")[1]
    dbrequests.upd_ulang_db(callback.from_user.id, dbrequests.userslang[callback.from_user.id])
    await callback.message.delete()
    await callback.message.answer(
        text=lang.set_lang_done[dbrequests.userslang[callback.from_user.id]],
        reply_markup=await kb.get_main_kb(dbrequests.userslang[callback.from_user.id])
    )
    await callback.answer()


@router.message(F.text.in_(lang.change_timediff.values()))
async def set_timediff(message: types.Message, state: FSMContext):
    await message.answer(
        text="Please give your time in format:",
        reply_markup=await kb.cancel_all_kb(dbrequests.userslang[message.from_user.id])
    )
    await state.clear()
    await state.set_state(TimeDiffSet.utimediff)


@router.message(TimeDiffSet.utimediff)
async def put_timediff(message: types.Message, state: FSMContext):
    if tim := get_time_difference(message.text):
        dbrequests.upd_utimediff_db(message.from_user.id, tim)
        await state.clear()
        await message.answer(
            "saved",
            reply_markup=await kb.get_main_kb(dbrequests.userslang[message.from_user.id])
        )
        return
    await set_timediff(message, state)


@router.message(F.text.in_(lang.settings.values()))
async def show_settings(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "here are the settings",
        reply_markup=await kb.get_settings_kb(dbrequests.userslang[message.from_user.id])
    )