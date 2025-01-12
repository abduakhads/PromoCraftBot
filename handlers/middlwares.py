from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Update, Message

import lang
from database import dbrequests
import keyboards as kb

class CancellForAll(BaseMiddleware):
    async def __call__(
            self, 
            handler: Callable[[Message, Dict[str, Any]], Awaitable], 
            event: Message | Update,
            data: Dict[str, Any]
        ) -> Any:
        if not event.from_user.id in dbrequests.userslang:
            await event.answer(
                "please restart bot -> /start"
            )
            return
        if event.text == lang.cancel_all[dbrequests.userslang[event.from_user.id]]:
            await data["state"].clear()
            await event.answer(
                lang.cancel_done[dbrequests.userslang[event.from_user.id]],
                reply_markup=await kb.get_main_kb(dbrequests.userslang[event.from_user.id])
            )
        else:
            return await handler(event, data)
            # return await super().__call__(handler, event, data)