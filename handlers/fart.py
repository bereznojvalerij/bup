from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database import get_user_id, add_event, get_all_users
from config import MAX_FART_PER_INPUT

router = Router()


class FartState(StatesGroup):
    waiting_for_count = State()


@router.message(lambda msg: msg.text == "💨 Пук")
async def fart_start(message: Message, state: FSMContext):
    await state.set_state(FartState.waiting_for_count)
    await message.answer("Введи количество:")


@router.message(FartState.waiting_for_count)
async def process_count(message: Message, state: FSMContext):
    try:
        count = int(message.text)
    except:
        await message.answer("Введи число")
        return

    if count <= 0 or count > MAX_FART_PER_INPUT:
        await message.answer("Недопустимое значение")
        return

    user_id = await get_user_id(message.from_user.id)
    await add_event(user_id, count)

    users = await get_all_users()

    text = f"💨 Только что {message.from_user.first_name} сделал {count} пук(а)!"

    for tg_id, _ in users:
        try:
            await message.bot.send_message(tg_id, text)
        except:
            pass

    await state.clear()