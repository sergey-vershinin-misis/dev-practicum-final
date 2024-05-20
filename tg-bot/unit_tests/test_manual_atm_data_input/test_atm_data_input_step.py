from unittest.mock import patch, AsyncMock

import pytest

from scenarios.manual_atm_data_input import AtmDataInputStep, AtmCoordsInputStep, States, AtmAddressInputStep
from unit_tests.mock_helpers import get_fsm_context_and_message_mock, get_text, get_buttons


@pytest.mark.asyncio
async def test_init_clears_state_data():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    await AtmDataInputStep.init(message, fsm_context)

    data = await fsm_context.get_data()
    assert list(data.keys()) == []


@pytest.mark.asyncio
async def test_init_sets_correct_state():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    await AtmDataInputStep.init(message, fsm_context)

    assert States.atm_data_input == await fsm_context.get_state()


@pytest.mark.asyncio
async def test_init_reply_with_correct_answer_and_keyboard():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    await AtmDataInputStep.init(message, fsm_context)

    assert (get_text(message.answer) ==
            "Выберите один из предложенных в меню ниже способов определения местоположения банкомата.")
    btn1, btn2 = get_buttons(message.answer)
    assert btn1.text == '1. Указать координаты'
    assert btn2.text == '2. Указать адрес'


@pytest.mark.asyncio
async def test_start_input_with_coords_inits_correct_step():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    with patch.object(AtmCoordsInputStep, "init", new=AsyncMock()):
        await AtmDataInputStep.start_input_with_coords(message, fsm_context)
        AtmCoordsInputStep.init.assert_awaited_once_with(message, fsm_context)


@pytest.mark.asyncio
async def test_start_input_with_address_inits_correct_step():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    with patch.object(AtmAddressInputStep, "init", new=AsyncMock()):
        await AtmDataInputStep.start_input_with_address(message, fsm_context)
        AtmAddressInputStep.init.assert_awaited_once_with(message, fsm_context)


@pytest.mark.asyncio
async def test_incorrect_input_replies_with_proper_message_and_does_not_affect_state():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)
    old_state = await fsm_context.get_state()
    old_data = await fsm_context.get_data()

    await AtmDataInputStep.incorrect_input(message, fsm_context)

    assert old_state == await fsm_context.get_state()
    assert old_data == await fsm_context.get_data()
    message.reply.assert_awaited_once_with("Пожалуйста, выберите один из предложенных в меню вариантов действия")
