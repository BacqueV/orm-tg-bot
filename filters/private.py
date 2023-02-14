from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsPrivate(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        current_chat = message.chat.type
        private_chat = type(types.ChatType.PRIVATE)
        return isinstance(current_chat, private_chat)
