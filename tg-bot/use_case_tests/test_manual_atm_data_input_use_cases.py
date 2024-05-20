from unittest.mock import patch

import pytest

from scenarios.manual_atm_data_input import AtmDataInputStep, AtmCoordsInputStep, States, \
    AtmLocationConfirmationStep, AtmGroupInputStep, AtmAddressInputStep
from service_adapters.dadata_adapter import DadataAdapter
from service_adapters.prediction_service_adapter import PredictionServiceAdapter
from unit_tests.mock_helpers import get_fsm_context_and_message_mock, get_text, get_buttons
from unit_tests.data_helpers import get_address_data, get_atm_groups


@pytest.mark.asyncio
async def test_manual_atm_data_input_using_coords_use_case():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    await AtmDataInputStep.init(message, fsm_context)
    assert States.atm_data_input == await fsm_context.get_state()
    btn1, btn2 = get_buttons(message.answer)
    assert btn1.text == '1. Указать координаты'
    assert btn2.text == '2. Указать адрес'
    message.reset_mock()

    await AtmDataInputStep.start_input_with_coords(message, fsm_context)
    assert States.atm_coords_input == await fsm_context.get_state()
    assert get_text(message.answer).startswith('Введите широту и долготу места для размещения банкомата')
    message.reset_mock()

    addr_data = get_address_data()
    with patch.object(DadataAdapter, 'get_data_by_coords', return_value=addr_data):
        message.text = "0.0 1.1"
        await AtmCoordsInputStep.input_lat_lon(message, fsm_context)
    data = await fsm_context.get_data()
    assert data['address_data'] == addr_data
    assert States.atm_location_confirmation == await fsm_context.get_state()
    message.reset_mock()

    with patch.object(PredictionServiceAdapter, 'get_atm_groups', return_value=get_atm_groups()):
        await AtmLocationConfirmationStep.confirm_data(message, fsm_context)
    assert States.atm_group_input == await fsm_context.get_state()
    btn1, btn2 = get_buttons(message.reply)
    assert btn1.text == get_atm_groups()[0]
    assert btn2.text == get_atm_groups()[1]
    message.reset_mock()

    atm_group = get_atm_groups()[0]
    message.text = atm_group
    prediction = 0
    with patch.object(PredictionServiceAdapter, 'predict_one', return_value=prediction):
        await AtmGroupInputStep.input_atm_group(message, fsm_context)
    data = await fsm_context.get_data()
    assert data['atm_group'] == atm_group
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


@pytest.mark.asyncio
async def test_manual_atm_data_input_using_address_use_case():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    await AtmDataInputStep.init(message, fsm_context)
    assert States.atm_data_input == await fsm_context.get_state()
    btn1, btn2 = get_buttons(message.answer)
    assert btn1.text == '1. Указать координаты'
    assert btn2.text == '2. Указать адрес'
    message.reset_mock()

    await AtmDataInputStep.start_input_with_address(message, fsm_context)
    assert States.atm_address_input == await fsm_context.get_state()
    assert get_text(message.answer).startswith('Введите адрес банкомата одной строкой')
    message.reset_mock()

    addr_data = get_address_data()
    with patch.object(DadataAdapter, 'get_data_by_address', return_value=addr_data):
        message.text = "Адрес объекта"
        await AtmAddressInputStep.input_address(message, fsm_context)
    data = await fsm_context.get_data()
    assert data['address_data'] == addr_data
    assert States.atm_location_confirmation == await fsm_context.get_state()
    message.reset_mock()

    with patch.object(PredictionServiceAdapter, 'get_atm_groups', return_value=get_atm_groups()):
        await AtmLocationConfirmationStep.confirm_data(message, fsm_context)
    assert States.atm_group_input == await fsm_context.get_state()
    btn1, btn2 = get_buttons(message.reply)
    assert btn1.text == get_atm_groups()[0]
    assert btn2.text == get_atm_groups()[1]
    message.reset_mock()

    atm_group = get_atm_groups()[0]
    message.text = atm_group
    prediction = 0
    with patch.object(PredictionServiceAdapter, 'predict_one', return_value=prediction):
        await AtmGroupInputStep.input_atm_group(message, fsm_context)
    data = await fsm_context.get_data()
    assert data['atm_group'] == atm_group
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
