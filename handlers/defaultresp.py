from aiogram import Router, types

from handlers.middlwares import CancellForAll

router = Router()
router.message.middleware(CancellForAll())


@router.message()
async def defaults(message: types.Message):
    await message.answer(":)")