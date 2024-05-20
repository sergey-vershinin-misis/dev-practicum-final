from unittest.mock import patch, AsyncMock

import pytest

from scenarios import upload_csv_with_atm_data
from scenarios.upload_csv_with_atm_data import ResultDownloadStep, DataUploadStep
from unit_tests.mock_helpers import get_fsm_context_and_message_mock, get_buttons, get_call_info


@pytest.mark.asyncio
async def test_init_sets_correct_state_send_file_and_reply_with_proper_answer():
    fsm_context, message = await get_fsm_context_and_message_mock()
    output_file = AsyncMock()
    await fsm_context.update_data(output_file=output_file)

    await ResultDownloadStep.init(message, fsm_context)

    assert (get_call_info(message.answer_document).args[0] == output_file)
    assert (get_call_info(message.answer_document).kwargs['caption'] ==
            "Результаты предсказания индекса популярности были добавлены в ваш csv-файл")

    btn1, btn2 = get_buttons(message.answer_document)
    assert btn1.text == '1. Загрузить новый файл'
    assert btn2.text == '2. Вернуться к началу'


@pytest.mark.asyncio
async def test_upload_new_file_inits_correct_step():
    fsm_context, message = await get_fsm_context_and_message_mock()

    with patch.object(DataUploadStep, "init", new=AsyncMock()):
        await ResultDownloadStep.upload_new_file(message, fsm_context)
        DataUploadStep.init.assert_awaited_once_with(message, fsm_context)


@pytest.mark.asyncio
async def test_restart_bot_makes_bot_to_send_start_message():
    fsm_context, message = await get_fsm_context_and_message_mock()

    with patch.object(upload_csv_with_atm_data, "show_start_message", new=AsyncMock()):
        await ResultDownloadStep.restart_bot(message, fsm_context)
        upload_csv_with_atm_data.show_start_message.assert_awaited_once_with(message, fsm_context)
