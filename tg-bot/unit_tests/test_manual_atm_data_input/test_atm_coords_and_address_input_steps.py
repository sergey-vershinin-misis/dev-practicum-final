from unittest.mock import patch, AsyncMock, Mock

import pytest
from aiogram.types import ReplyKeyboardRemove

from scenarios.manual_atm_data_input import (
    States,
    AtmCoordsInputStep,
    AtmLocationConfirmationStep,
    AtmAddressInputStep
)
from service_adapters import dadata_adapter
from unit_tests.mock_helpers import get_fsm_context_and_message_mock, get_text, get_reply_markup
from unit_tests.data_helpers import get_address_data, get_imprecise_addr_data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "step_class, state",
    [
        (AtmCoordsInputStep, States.atm_coords_input),
        (AtmAddressInputStep, States.atm_address_input)
    ]
)
async def test_init_sets_correct_state(step_class, state):
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    await step_class.init(message, fsm_context)

    assert state == await fsm_context.get_state()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "step_class, answer_text",
    [
        (AtmCoordsInputStep, 'Введите широту и долготу места для размещения банкомата'),
        (AtmAddressInputStep, 'Введите адрес банкомата одной строкой')
    ]
)
async def test_init_reply_with_correct_answer_and_keyboard(step_class, answer_text):
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    await step_class.init(message, fsm_context)

    assert get_text(message.answer).startswith(answer_text)
    assert get_reply_markup(message.answer) == ReplyKeyboardRemove()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "step_class_method, dadata_adapter_search_method",
    [
        (AtmCoordsInputStep.input_lat_lon, 'get_data_by_coords'),
        (AtmAddressInputStep.input_address, 'get_data_by_address'),
    ]
)
async def test_input_coords_and_address_save_state_data_and_init_location_confirmation_step(
        step_class_method,
        dadata_adapter_search_method
):
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)
    message.text = "1.1 0.0"
    addr = get_address_data()

    with (
        patch.object(dadata_adapter.DadataAdapter, dadata_adapter_search_method, return_value=addr),
        patch.object(AtmLocationConfirmationStep, "init", new=AsyncMock())
    ):
        await step_class_method(message, fsm_context)
        AtmLocationConfirmationStep.init.assert_awaited_once_with(message, fsm_context)

    data = await fsm_context.get_data()
    assert data['address_data'] == addr


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "step_class_method, dadata_adapter_search_method",
    [
        (AtmCoordsInputStep.input_lat_lon, 'get_data_by_coords'),
        (AtmAddressInputStep.input_address, 'get_data_by_address'),
    ]
)
async def test_input_coords_and_address_reply_properly_when_address_is_not_found(
        step_class_method,
        dadata_adapter_search_method
):
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)
    message.text = "1.1 0.0"

    with patch.object(dadata_adapter.DadataAdapter, dadata_adapter_search_method, return_value=None):
        await step_class_method(message, fsm_context)

    message.reply.assert_awaited_once_with("К сожалению, нам не удалось найти необходимую информацию "
                                           "об указанном местоположении."
                                           "Попробуйте ввести более точный адрес или координаты.")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "step_class_method, dadata_adapter_search_method",
    [
        (AtmCoordsInputStep.input_lat_lon, 'get_data_by_coords'),
        (AtmAddressInputStep.input_address, 'get_data_by_address'),
    ]
)
async def test_input_coords_and_address_reply_properly_when_address_is_not_precise(
        step_class_method,
        dadata_adapter_search_method
):
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)
    message.text = "1.1 0.0"
    incorrect_addr = get_imprecise_addr_data()

    with patch.object(dadata_adapter.DadataAdapter, dadata_adapter_search_method, return_value=incorrect_addr):
        await step_class_method(message, fsm_context)

    message.reply.assert_awaited_once_with('К сожалению, нам не удалось определить точное '
                                           'расположение указанного места размещения.'
                                           'Попробуйте ввести более точный адрес или координаты.')


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "step_class_method, dadata_adapter_search_method, answer_text",
    [
        (
                AtmCoordsInputStep.input_lat_lon,
                'get_data_by_coords',
                'К сожалению, мы не смогли обработать введенные координаты. Попробуйте повторить ввод'
        ),
        (
                AtmAddressInputStep.input_address,
                'get_data_by_address',
                'К сожалению нам не удалось получить необходимую информацию о вашем адресе. '
                'Попробуйте ввести другой адрес.'
        ),
    ]
)
async def test_input_coords_and_address_reply_properly_when_dadata_adapter_raise_error(
        step_class_method,
        dadata_adapter_search_method,
        answer_text
):
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)
    message.text = "1.1 0.0"
    raise_error_mock = Mock()
    raise_error_mock.side_effect = ValueError

    with patch.object(dadata_adapter.DadataAdapter, dadata_adapter_search_method, raise_error_mock):
        await step_class_method(message, fsm_context)

    message.reply.assert_awaited_once_with(answer_text)


@pytest.mark.asyncio
async def test_input_coords_reply_properly_when_coords_format_is_incorrect():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)
    message.text = "coords"
    await AtmCoordsInputStep.input_lat_lon(message, fsm_context)
    message.reply.assert_awaited_once_with(
        'К сожалению, мы не смогли обработать введенные координаты. Попробуйте повторить ввод')
