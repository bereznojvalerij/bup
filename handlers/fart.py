from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database import get_user_id, add_event, get_all_users
from config import MAX_FART_PER_INPUT
from keyboards.main import fart_keyboard, main_keyboard

router = Router()


class FartState(StatesGroup):
    waiting_for_count = State()


@router.callback_query(lambda c: c.data == "fart")
async def fart_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выбери количество:",
        reply_markup=fart_keyboard()
    )

@router.callback_query(lambda c: c.data.startswith("fart_"))
async def add_fart(callback: CallbackQuery):
    count = int(callback.data.split("_")[1])

    user_id = await get_user_id(callback.from_user.id)
    await add_event(user_id, count)

    text = f"💨 {callback.from_user.first_name} сделал {count} пук(а)!"

    await callback.message.answer(text, reply_markup=main_keyboard())

    await callback.message.edit_text(
        "Меню:",
        reply_markup=main_keyboard()
    )

@router.callback_query(lambda c: c.data == "back")
async def back(callback: CallbackQuery):
    await callback.message.edit_text(
        "Меню:",
        reply_markup=main_keyboard()
    )