from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject, Update
from typing import Callable, Dict, Any, Awaitable
from botcore.untils import get_chat_db, update_chat
from typing import Union


class ChatMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:

        if event.message:
            chat = event.message.from_user
        elif event.callback_query:
            chat = event.callback_query.from_user

        chat = update_chat(chat)
        data["chat_db"] = chat

        if not chat.block:
            return await handler(event, data)


class AdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:

        if event.message:
            chat = event.message.from_user
        elif event.callback_query:
            chat = event.callback_query.from_user

        chat = get_chat_db(chat.id)
        if chat.is_support or event.text.lower() == '/start' or chat.is_admin:
            return await handler(event, data)
