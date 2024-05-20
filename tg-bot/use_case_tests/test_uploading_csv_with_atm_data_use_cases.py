from unittest.mock import patch, AsyncMock

import pytest
from aiogram.types import BufferedInputFile

from scenarios.upload_csv_with_atm_data import DataUploadStep, States
from service_adapters.prediction_service_adapter import PredictionServiceAdapter
from unit_tests.mock_helpers import get_fsm_context_and_message_mock, get_call_info
from unit_tests.test_upload_csv_with_atm_data.test_data_upload_step import get_full_filename


@pytest.mark.asyncio
async def test_uploading_csv_with_atm_data_use_case():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    await DataUploadStep.init(message, fsm_context)
    assert States.data_upload == await fsm_context.get_state()
    message.reset_mock()

    filename = 'atm_data_sample.csv'
    message.document.file_name = filename
    bot = AsyncMock()

    with (
        open(get_full_filename(filename), 'rb') as sample_file,
        patch.object(bot, 'download', return_value=sample_file),
        patch.object(PredictionServiceAdapter, 'predict_many', return_value=[0, 0, 0, 0, 0])

    ):
        await DataUploadStep.upload_and_process_file(message, bot, fsm_context)

        output_file: BufferedInputFile = get_call_info(message.answer_document).args[0]
        assert isinstance(output_file, BufferedInputFile)

        actual_csv_str = output_file.data.decode("utf-8").replace("\r\n", "\n")
        with open(get_full_filename('atm_data_sample_with_target.csv')) as f:
            expected_csv_str = f.read().replace("\r\n", "\n")
            assert expected_csv_str == actual_csv_str
