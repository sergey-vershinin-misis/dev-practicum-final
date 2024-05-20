import csv
import io

from aiogram import Bot, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, BufferedInputFile, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from pydantic import ValidationError

from scenarios.manual_atm_data_input import AtmGroupInputStep
from service_adapters.prediction_service_adapter import AtmData, PredictionServiceAdapter
from scenarios.scenario_selection import show_start_message


class States(StatesGroup):
    data_upload = State()
    results_download = State()


router = Router()


class DataUploadStep:
    @staticmethod
    @router.message(Command("upload_csv"))
    async def init(message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(States.data_upload)
        await message.answer(
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
                 + f"{', '.join(AtmGroupInputStep.get_atm_groups())}",
            reply_markup=ReplyKeyboardRemove()
        )

    @staticmethod
    @router.message(StateFilter(States.data_upload))
    async def upload_and_process_file(message: Message, bot: Bot, state: FSMContext):
        try:
            document = message.document
            input_file = await bot.download(document)
            reader = csv.DictReader(io.TextIOWrapper(input_file))

            atm_data_list = [AtmData.model_validate(row) for row in reader]
            results = PredictionServiceAdapter.predict_many(atm_data_list)
            if (results is None) or (len(results) == 0):
                await message.reply("К сожалению мы не смогли обработать данные в переданном файле. Пожалуйста, "
                                    "отправьте другой файл или повторите попытку позже")
            else:
                atm_data_dict_list = []
                for i, atm_data in enumerate(atm_data_list):
                    d = atm_data.model_dump()
                    d['target'] = results[i]
                    atm_data_dict_list.append(d)

                csv_data = io.StringIO()
                writer = csv.DictWriter(csv_data, fieldnames=atm_data_dict_list[0].keys())
                writer.writeheader()
                writer.writerows(atm_data_dict_list)

                output_file = BufferedInputFile(
                    csv_data.getvalue().encode(),
                    filename=document.file_name.replace(".", "_with_target.", 1)
                )

                await state.update_data(output_file=output_file)
                await ResultDownloadStep.init(message, state)

        except ValidationError as err:
            print(err)
            await message.reply("К сожалению формат данных в файле не соответствует ожидаемому")
        except Exception as e:
            print(e)
            await message.reply("К сожалению мы не смогли обработать введенные данные. Попробуйте еще раз.")


class ResultDownloadStep:
    @staticmethod
    async def init(message: Message, state: FSMContext):
        await state.set_state(States.results_download)
        data = await state.get_data()

        await message.answer_document(
            data['output_file'],
            caption="Результаты предсказания индекса популярности были добавлены в ваш csv-файл",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=t) for t in ("1. Загрузить новый файл", "2. Вернуться к началу")]],
                resize_keyboard=True)
        )

    @staticmethod
    @router.message(StateFilter(States.results_download), F.text.startswith("1."))
    async def upload_new_file(message: Message, state: FSMContext):
        await DataUploadStep.init(message, state)

    @staticmethod
    @router.message(StateFilter(States.results_download), F.text.startswith("2."))
    async def restart_bot(message: Message, state: FSMContext):
        await show_start_message(message, state)
