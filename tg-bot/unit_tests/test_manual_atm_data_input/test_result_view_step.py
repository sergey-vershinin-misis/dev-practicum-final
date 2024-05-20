from unittest.mock import patch, AsyncMock

import pytest

from scenarios import manual_atm_data_input
from scenarios.manual_atm_data_input import AtmDataInputStep, States, ResultViewStep
from service_adapters.prediction_service_adapter import PredictionServiceAdapter
from unit_tests.mock_helpers import get_fsm_context_and_message_mock, get_text, get_buttons
from unit_tests.data_helpers import get_address_data


@pytest.mark.asyncio
async def test_init_sets_correct_state_and_reply_with_correct_answer_and_keyboard():
    fsm_context, message = await get_fsm_context_and_message_mock()
    addr_data = get_address_data()
    atm_group = 'group'
    await fsm_context.update_data(address_data=addr_data)
    await fsm_context.update_data(atm_group=atm_group)
    prediction = 2

    with patch.object(PredictionServiceAdapter, 'predict_one', return_value=prediction):
        await ResultViewStep.init(message, fsm_context)

    assert States.result_view == await fsm_context.get_state()
    assert (get_text(message.answer) ==
            f"Вы ввели следующие данные о банкомате:\n"
            f"\n"
            f"<code>"
            f"Координаты: {addr_data.lat}, {addr_data.lon}\n"
            f"Адрес: {addr_data.address}\n"
            f"Банковская группа: {atm_group}\n"
            f"</code>"
            f"\n"
            f"Предсказанное значение индекса популярности равно:\n"
            f"<code>"
            f"{prediction}"
            f"</code>"
            f"\n"
            f"\n"
            f"Хотите получить предсказание для еще одного банкомата?\n")
    btn1, btn2 = get_buttons(message.answer)
    assert btn1.text == '1. Еще одно предсказание'
    assert btn2.text == '2. Вернуться к началу'


@pytest.mark.asyncio
async def test_input_new_atm_data_inits_correct_step():
    fsm_context, message = await get_fsm_context_and_message_mock()

    with patch.object(AtmDataInputStep, "init", new=AsyncMock()):
        await ResultViewStep.input_new_atm_data(message, fsm_context)
        AtmDataInputStep.init.assert_awaited_once_with(message, fsm_context)


@pytest.mark.asyncio
async def test_restart_bot_makes_bot_to_send_start_message():
    fsm_context, message = await get_fsm_context_and_message_mock()

    with patch.object(manual_atm_data_input, "show_start_message", new=AsyncMock()):
        await ResultViewStep.restart_bot(message, fsm_context)
        manual_atm_data_input.show_start_message.assert_awaited_once_with(message, fsm_context)
