from aiogram import Router
from aiogram.types import Message

from database import add_user

router = Router()


@router.message()
async def register_user(message: Message):

    await add_user(
        message.from_user.id,
        message.from_user.first_name,
        message.chat.id
    )