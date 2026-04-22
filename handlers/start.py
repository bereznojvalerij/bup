from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from database import add_user
from keyboards.main import main_keyboard

router = Router()


@router.message(CommandStart())
async def start_private(message: Message):

    await add_user(
        message.from_user.id,
        message.from_user.first_name,
        message.chat.id
    )

    if message.chat.type == "private":
        await message.answer("Меню", reply_markup=main_keyboard())
    else:
        await message.answer("Бот активирован в группе. Используй /puk N")


@router.message(lambda msg: msg.text and msg.text.startswith("/start"))
async def start_group(message: Message):

    await add_user(
        message.from_user.id,
        message.from_user.first_name,
        message.chat.id
    )

    await message.answer("Бот активирован в группе. Используй /puk N")