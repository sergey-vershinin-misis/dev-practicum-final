from unittest.mock import patch, AsyncMock

import pytest
from aiogram.types import ReplyKeyboardRemove, BufferedInputFile

from scenarios.manual_atm_data_input import AtmGroupInputStep
from scenarios.upload_csv_with_atm_data import DataUploadStep, States, ResultDownloadStep
from service_adapters.prediction_service_adapter import PredictionServiceAdapter
from unit_tests.mock_helpers import get_fsm_context_and_message_mock
from unit_tests.data_helpers import get_atm_groups


@pytest.mark.asyncio
async def test_init_clears_state_data():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    await DataUploadStep.init(message, fsm_context)

    data = await fsm_context.get_data()
    assert list(data.keys()) == []


@pytest.mark.asyncio
async def test_init_sets_correct_state():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    await DataUploadStep.init(message, fsm_context)

    assert States.data_upload == await fsm_context.get_state()


@pytest.mark.asyncio
async def test_init_reply_with_correct_answer_and_keyboard():
    fsm_context, message = await get_fsm_context_and_message_mock(dirty_state=True)

    atm_groups = get_atm_groups()
    with patch.object(AtmGroupInputStep, 'get_atm_groups', return_value=atm_groups):
        await DataUploadStep.init(message, fsm_context)

    message.answer.assert_awaited_once_with(
        text="Отправьте CSV-файл, содержащий необходимые для предсказания индекса популярности "
             "данные о банкомате.\n"
             "Пример содержимого файла:\n"
             "\n"
             "<code>"
             "lat,lon,atm_group\n"
             "55.878,37.653,Rosbank\n"
             "54.704,56.006,Alfabank\n"
             "</code>\n"
             "Для задания банковской группы (atm_group) вы можете использовать следующие значения:\n"
             + f"{', '.join(atm_groups)}",
        reply_markup=ReplyKeyboardRemove()
    )


def get_full_filename(filename):
    return f'unit_tests/test_upload_csv_with_atm_data/{filename}'


@pytest.mark.asyncio
async def test_upload_and_process_file_creates_correct_output_file():
    fsm_context, message = await get_fsm_context_and_message_mock()
    filename = 'atm_data_sample.csv'
    message.document.file_name = filename
    with open(get_full_filename('atm_data_sample_with_target.csv')) as f:
        expected_csv_str = f.read().replace("\r\n", "\n")

    bot = AsyncMock()

    with (
        open(get_full_filename(filename), 'rb') as sample_file,
        patch.object(bot, 'download', return_value=sample_file),
        patch.object(ResultDownloadStep, 'init', new=AsyncMock()),
        patch.object(PredictionServiceAdapter, 'predict_many', return_value=[0, 0, 0, 0, 0])

    ):
        await DataUploadStep.upload_and_process_file(message, bot, fsm_context)
        data = await fsm_context.get_data()
        output_file: BufferedInputFile = data['output_file']
        assert isinstance(output_file, BufferedInputFile)

        actual_csv_str = output_file.data.decode("utf-8").replace("\r\n", "\n")

        assert expected_csv_str == actual_csv_str
        ResultDownloadStep.init.assert_awaited_once_with(message, fsm_context)


@pytest.mark.parametrize(
    "prediction_service_results", [None, []]
)
@pytest.mark.asyncio
async def test_upload_and_process_file_answers_correctly_when_prediction_service_returns_unexpected_data(
        prediction_service_results
):
    fsm_context, message = await get_fsm_context_and_message_mock()
    filename = 'atm_data_sample.csv'
    message.document.file_name = filename
    bot = AsyncMock()

    with (
        open(get_full_filename(filename), 'rb') as sample_file,
        patch.object(bot, 'download', return_value=sample_file),
        patch.object(PredictionServiceAdapter, 'predict_many', return_value=prediction_service_results)

    ):
        await DataUploadStep.upload_and_process_file(message, bot, fsm_context)
        message.reply.assert_awaited_once_with("К сожалению мы не смогли обработать данные в "
                                               "переданном файле. Пожалуйста, "
                                               "отправьте другой файл или повторите попытку позже")


@pytest.mark.asyncio
async def test_upload_and_process_file_answers_correctly_when_input_csv_file_has_invalid_data():
    fsm_context, message = await get_fsm_context_and_message_mock()
    filename = 'atm_data_sample_invalid.csv'
    message.document.file_name = filename
    bot = AsyncMock()

    with (
        open(get_full_filename(filename), 'rb') as sample_file,
        patch.object(bot, 'download', return_value=sample_file),
        patch.object(PredictionServiceAdapter, 'predict_many', return_value=[0, 0, 0, 0, 0])

    ):
        await DataUploadStep.upload_and_process_file(message, bot, fsm_context)
        message.reply.assert_awaited_once_with("К сожалению формат данных в файле не соответствует ожидаемому")
