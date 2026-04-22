from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database import get_user_id, add_event, get_all_users
from config import MAX_FART_PER_INPUT
from keyboards.main import fart_keyboard, main_keyboard

router = Router()


class FartState(StatesGroup):
    waiting_for_count = State()


@router.message(lambda msg: msg.text == "💨 Пук")
async def fart_menu(message: Message):
    await message.answer(
        "Выбери количество:",
        reply_markup=fart_keyboard()
    )

@router.message(lambda msg: msg.text in ["+1", "+2", "+3", "+4", "+5", "+6"])
async def add_fart(message: Message):
    count = int(message.text.replace("+", ""))

    user_id = await get_user_id(message.from_user.id)
    await add_event(user_id, count)

    users = await get_all_users()

    text = f"💨 Только что {message.from_user.first_name} сделал {count} пук(а)!"

    for tg_id, _ in users:
        try:
            await message.bot.send_message(tg_id, text)
        except:
            pass

    await message.answer("Записано ✅", reply_markup=main_keyboard())

@router.message(lambda msg: msg.text == "⬅️ Назад")
async def back(message: Message):
    await message.answer("Главное меню", reply_markup=main_keyboard())