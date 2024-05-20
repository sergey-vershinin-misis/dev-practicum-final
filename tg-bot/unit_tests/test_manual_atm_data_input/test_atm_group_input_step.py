from unittest.mock import patch, AsyncMock

import pytest

from scenarios.manual_atm_data_input import States, AtmGroupInputStep, ResultViewStep
from service_adapters.prediction_service_adapter import PredictionServiceAdapter
from unit_tests.mock_helpers import get_fsm_context_and_message_mock, get_text, get_buttons
from unit_tests.data_helpers import get_atm_groups


@pytest.mark.asyncio
async def test_init_sets_correct_state():
    fsm_context, message = await get_fsm_context_and_message_mock()

    with patch.object(PredictionServiceAdapter, 'get_atm_groups', return_value=get_atm_groups()):
        await AtmGroupInputStep.init(message, fsm_context)

    assert States.atm_group_input == await fsm_context.get_state()


@pytest.mark.asyncio
async def test_init_reply_with_correct_answer_and_keyboard():
    fsm_context, message = await get_fsm_context_and_message_mock()
    with patch.object(PredictionServiceAdapter, 'get_atm_groups', return_value=get_atm_groups()):
        await AtmGroupInputStep.init(message, fsm_context)

    assert get_text(message.reply) == 'Выберите банковскую группу, банкомат которой планируется разместить:'
    btn1, btn2 = get_buttons(message.reply)
    assert btn1.text == get_atm_groups()[0]
    assert btn2.text == get_atm_groups()[1]


@pytest.mark.asyncio
async def test_input_atm_group_save_group_and_init_correct_step_when_input_is_valid():
    fsm_context, message = await get_fsm_context_and_message_mock()
    atm_group = get_atm_groups()[0]
    message.text = atm_group
    with patch.object(PredictionServiceAdapter, 'get_atm_groups', return_value=get_atm_groups()):
        with patch.object(ResultViewStep, "init", new=AsyncMock()):
            await AtmGroupInputStep.input_atm_group(message, fsm_context)

            ResultViewStep.init.assert_awaited_once_with(message, fsm_context)
            data = await fsm_context.get_data()
            assert atm_group == data['atm_group']


@pytest.mark.asyncio
async def test_input_atm_group_reply_with_correct_answer_when_input_is_invalid():
    fsm_context, message = await get_fsm_context_and_message_mock()
    message.text = "none"
    with patch.object(PredictionServiceAdapter, 'get_atm_groups', return_value=get_atm_groups()):
        await AtmGroupInputStep.input_atm_group(message, fsm_context)

    message.reply.assert_awaited_once_with('Пожалуйста, выберите одну из предложенных групп')
