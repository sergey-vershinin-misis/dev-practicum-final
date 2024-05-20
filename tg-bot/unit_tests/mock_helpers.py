from unittest.mock import AsyncMock

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage


async def get_fsm_context_and_message_mock(dirty_state: bool = False):
    return await get_empty_state(dirty_state=dirty_state), AsyncMock()


async def get_empty_state(dirty_state: bool = False) -> FSMContext:
    state = FSMContext(MemoryStorage(), StorageKey(chat_id=42, user_id=42, bot_id=42))
    if dirty_state:
        await state.set_data({'garbage': 'full'})
        await state.set_state(State(state='fake_state'))
    return state


def get_text(bot_response_method_mock) -> str:
    return str(get_call_info(bot_response_method_mock).args[0])


def get_reply_markup(bot_response_method_mock):
    return get_call_info(bot_response_method_mock).kwargs['reply_markup']


def get_buttons(bot_response_method_mock):
    keyboard = get_reply_markup(bot_response_method_mock).keyboard
    assert len(keyboard) == 1
    return keyboard[0]


def get_call_info(method_mock):
    assert len(method_mock.await_args_list) == 1
    return method_mock.await_args_list[0]
