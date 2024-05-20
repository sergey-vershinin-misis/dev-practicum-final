import pytest

from scenarios.show_model_info import show_model_info
from unit_tests.mock_helpers import get_fsm_context_and_message_mock


@pytest.mark.asyncio
async def test_show_model_info_reply_with_some_photo():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    await show_model_info(message, fsm_context)

    message.answer_photo.assert_awaited_once()
