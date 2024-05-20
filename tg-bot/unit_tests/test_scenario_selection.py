import pytest

from scenarios.scenario_selection import show_start_message
from unit_tests.mock_helpers import get_fsm_context_and_message_mock


@pytest.mark.asyncio
async def test_show_start_message_clears_state_data():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    await show_start_message(message, fsm_context)

    data = await fsm_context.get_data()
    assert list(data.keys()) == []


@pytest.mark.asyncio
async def test_show_start_message_reply_with_some_answer():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    await show_start_message(message, fsm_context)

    message.answer.assert_awaited_once()
