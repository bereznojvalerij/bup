from aiogram import Router
from aiogram.types import Message
from database import add_user
from keyboards.main import main_keyboard

router = Router()


@router.message(lambda msg: msg.text == "/start")
async def start_handler(message: Message):
    await add_user(message.from_user.id, message.from_user.first_name)

    await message.answer(
        "Добро пожаловать в систему учета 💨",
        reply_markup=main_keyboard()
    )