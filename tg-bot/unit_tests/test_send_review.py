from unittest.mock import AsyncMock, patch

import pytest

import scenarios.play_game
from configs.settings import settings
from scenarios.send_review import start_sending_review, States, process_review
from unit_tests.mock_helpers import get_fsm_context_and_message_mock


@pytest.mark.asyncio
async def test_start_sending_review_clears_state_data_and_sets_correct_state():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    await start_sending_review(message, fsm_context)

    data = await fsm_context.get_data()
    assert list(data.keys()) == []
    assert States.send_review_state == await fsm_context.get_state()


@pytest.mark.asyncio
async def test_process_review_forward_review_answers_properly_and_makes_bot_to_send_start_message():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    with patch.object(scenarios.send_review, "show_start_message", new=AsyncMock()):
        await process_review(message, fsm_context)
        message.forward.assert_awaited_once_with(chat_id=settings.atm_project_team_chat_id)
        message.answer.assert_awaited_once_with("Благодарим вас за отзыв о работе нашего сервиса")
        scenarios.send_review.show_start_message.assert_awaited_once_with(message, fsm_context)
