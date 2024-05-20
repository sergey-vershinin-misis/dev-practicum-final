from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from configs.settings import settings
from scenarios.scenario_selection import show_start_message

router = Router()


class States(StatesGroup):
    send_review_state = State()


@router.message(Command("send_review"))
async def start_sending_review(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(States.send_review_state)

    await message.answer(
        "Пожалуйста, отправьте сообщение с отзывом о работе бота и мы отправим его команде разработки",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(StateFilter(States.send_review_state))
async def process_review(message: Message, state: FSMContext):
    await message.forward(chat_id=settings.atm_project_team_chat_id)
    await message.answer("Благодарим вас за отзыв о работе нашего сервиса")
    await show_start_message(message, state)
