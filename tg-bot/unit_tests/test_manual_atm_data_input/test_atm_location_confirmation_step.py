from unittest.mock import patch, AsyncMock

import pytest

from scenarios.manual_atm_data_input import AtmDataInputStep, States, AtmLocationConfirmationStep, AtmGroupInputStep
from unit_tests.mock_helpers import get_fsm_context_and_message_mock, get_text, get_buttons
from unit_tests.data_helpers import get_address_data


@pytest.mark.asyncio
async def test_init_sets_correct_state():
    fsm_context, message = await get_fsm_context_and_message_mock()
    await fsm_context.update_data(address_data=get_address_data())

    await AtmLocationConfirmationStep.init(message, fsm_context)

    assert States.atm_location_confirmation == await fsm_context.get_state()


@pytest.mark.asyncio
async def test_init_reply_with_correct_answer_and_keyboard():
    fsm_context, message = await get_fsm_context_and_message_mock()
    address_data = get_address_data()
    await fsm_context.update_data(address_data=address_data)

    await AtmLocationConfirmationStep.init(message, fsm_context)

    assert (get_text(message.answer) ==
            f"Мы нашли следующую информацию об интересующем вас местоположении банкомата:\n"
            f"\n"
            f"<code>"
            f"Координаты: {address_data.lat}, {address_data.lon}\n"
            f"Адрес: {address_data.address}\n"
            f"</code>"
            f"\n"
            f"Пожалуйста, подтвердите, что данные корректны. Или введите данные заново.")
    btn1, btn2 = get_buttons(message.answer)
    assert btn1.text == '1. Данные корректны'
    assert btn2.text == '2. Хочу ввести данные заново'


@pytest.mark.asyncio
async def test_confirm_data_inits_correct_step():
    fsm_context, message = await get_fsm_context_and_message_mock()

    with patch.object(AtmGroupInputStep, "init", new=AsyncMock()):
        await AtmLocationConfirmationStep.confirm_data(message, fsm_context)
        AtmGroupInputStep.init.assert_awaited_once_with(message, fsm_context)


@pytest.mark.asyncio
async def test_repeat_input_inits_correct_step():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    with patch.object(AtmDataInputStep, "init", new=AsyncMock()):
        await AtmLocationConfirmationStep.repeat_input(message, fsm_context)
        AtmDataInputStep.init.assert_awaited_once_with(message, fsm_context)


@pytest.mark.asyncio
async def test_incorrect_input_replies_with_proper_message_and_does_not_affect_state():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)
    old_state = await fsm_context.get_state()
    old_data = await fsm_context.get_data()

    await AtmLocationConfirmationStep.incorrect_input(message)

    assert old_state == await fsm_context.get_state()
    assert old_data == await fsm_context.get_data()
    message.reply.assert_awaited_once_with("Пожалуйста, выберите один из предложенных в меню вариантов действия")
