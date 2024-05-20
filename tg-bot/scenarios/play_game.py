import time

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from scenarios.scenario_selection import show_start_message

router = Router()


class States(StatesGroup):
    game_state = State()


@router.message(Command("play"))
async def start_game(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(States.game_state)

    l, r = 1, 100
    guess = (l + r) // 2
    await state.update_data(rng=(l, r, guess))

    await message.answer(f"Загадайте число от {l} до {r}. И через несколько секунд я попробую его отгадать")
    time.sleep(3)
    await message.answer(
        f"Это число {guess}?",
        reply_markup=get_keyboard()
    )


@router.callback_query(StateFilter(States.game_state), F.data == "lower")
async def change_to_lower(callback: CallbackQuery, state: FSMContext):
    await make_new_guess(callback, state, lower=True)


@router.callback_query(StateFilter(States.game_state), F.data == "larger")
async def change_to_larger(callback: CallbackQuery, state: FSMContext):
    await make_new_guess(callback, state, lower=False)


async def make_new_guess(callback, state, lower: bool):
    data = await state.get_data()
    left, right, guess = data['rng']
    if lower:
        right = guess - 1
    else:
        left = guess + 1
    guess = (left + right) // 2
    await state.update_data(rng=(left, right, guess))
    await callback.message.edit_text(
        f"Это число {guess}?",
        reply_markup=get_keyboard()
    )


@router.callback_query(StateFilter(States.game_state), F.data == "equal")
async def end_game(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Ура, я угадал! Спасибо за игру!",
    )
    await show_start_message(callback.message, state)


def get_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Меньше",
            callback_data="lower"),
        InlineKeyboardButton(
            text="Больше",
            callback_data="larger"),
    )
    builder.row(
        InlineKeyboardButton(
            text="В самый раз",
            callback_data="equal"),
    )
    return builder.as_markup()
