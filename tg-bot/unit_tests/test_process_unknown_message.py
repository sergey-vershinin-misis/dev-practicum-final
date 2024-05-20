import pytest

from scenarios.process_unknown import process_unknown_message
from unit_tests.mock_helpers import get_fsm_context_and_message_mock


@pytest.mark.asyncio
async def test_process_unknown_message_returns_proper_answer():
    fsm_context, message = await get_fsm_context_and_message_mock()

    await process_unknown_message(message)

    message.reply.assert_awaited_once_with('К сожалению, мы не смогли обработать ваше сообщение. '
                                           'Пожалуйста, используйте одну из '
                                           'доступных команд бота')
