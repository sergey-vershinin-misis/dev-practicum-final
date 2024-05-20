import re

from aiogram import F, types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from scenarios.scenario_selection import show_start_message
from service_adapters.dadata_adapter import DadataAdapter, AddressData
from service_adapters.prediction_service_adapter import PredictionServiceAdapter, AtmData


class States(StatesGroup):
    atm_data_input = State()
    atm_location_type_input = State()
    atm_coords_input = State()
    atm_address_input = State()
    atm_location_confirmation = State()
    atm_group_input = State()
    result_view = State()


router = Router()


class AtmDataInputStep:
    @staticmethod
    @router.message(Command('manual_input'))
    async def init(message: Message, state: FSMContext) -> None:
        await state.clear()
        await state.set_state(States.atm_data_input)
        await message.answer(
            "Выберите один из предложенных в меню ниже способов определения местоположения банкомата.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=t) for t in ("1. Указать координаты", "2. Указать адрес")]],
                resize_keyboard=True)
        )

    @staticmethod
    @router.message(StateFilter(States.atm_data_input), F.text.startswith("1."))
    async def start_input_with_coords(message: types.Message, state: FSMContext):
        await AtmCoordsInputStep.init(message, state)

    @staticmethod
    @router.message(StateFilter(States.atm_data_input), F.text.startswith("2."))
    async def start_input_with_address(message: types.Message, state: FSMContext):
        await AtmAddressInputStep.init(message, state)

    @staticmethod
    @router.message(StateFilter(States.atm_data_input))
    async def incorrect_input(message: types.Message, state: FSMContext):
        await message.reply("Пожалуйста, выберите один из предложенных в меню вариантов действия")


class AtmCoordsInputStep:
    @staticmethod
    async def init(message: types.Message, state: FSMContext):
        await state.set_state(States.atm_coords_input)
        await message.answer(
            'Введите широту и долготу места для размещения банкомата'
            'В качестве разделителя целой и дробной частей координаты используйте точку.\n'
            '\n'
            'Пример ввода: <i>55.878 37.653</i>',
            reply_markup=ReplyKeyboardRemove()
        )

    @staticmethod
    @router.message(StateFilter(States.atm_coords_input))
    async def input_lat_lon(message: types.Message, state: FSMContext):
        try:
            lat, lon = map(float, re.findall(r"-?\d+\.*\d*", message.text))
            addr_data = DadataAdapter.get_data_by_coords(lat, lon)
            await AtmAddressInputStep.process_addr_data_search_results(addr_data, message, state)

        except ValueError:
            await message.reply(
                "К сожалению, мы не смогли обработать введенные координаты. Попробуйте повторить ввод")


class AtmAddressInputStep:
    @staticmethod
    async def init(message: types.Message, state: FSMContext):
        await state.set_state(States.atm_address_input)
        await message.answer(
            'Введите адрес банкомата одной строкой, указав город улицу и номер дома.\n'
            '\n'
            'Пример ввода: <i>Москва Сухонская 11</i>',
            reply_markup=ReplyKeyboardRemove()
        )

    @staticmethod
    @router.message(StateFilter(States.atm_address_input))
    async def input_address(message: types.Message, state: FSMContext):
        try:
            addr_data = DadataAdapter.get_data_by_address(message.text)
            await AtmAddressInputStep.process_addr_data_search_results(addr_data, message, state)
        except ValueError:
            await message.reply(
                "К сожалению нам не удалось получить необходимую информацию о вашем адресе. "
                "Попробуйте ввести другой адрес.")

    @staticmethod
    async def process_addr_data_search_results(addr_data, message, state):
        if addr_data is None:
            await message.reply(
                "К сожалению, нам не удалось найти необходимую информацию об указанном местоположении."
                "Попробуйте ввести более точный адрес или координаты.")
        elif addr_data.qc_geo > 1:
            await message.reply(
                "К сожалению, нам не удалось определить точное расположение указанного места размещения."
                "Попробуйте ввести более точный адрес или координаты.")
        else:
            await state.update_data(address_data=addr_data)
            await AtmLocationConfirmationStep.init(message, state)


class AtmLocationConfirmationStep:
    @staticmethod
    async def init(message: types.Message, state: FSMContext):
        await state.set_state(States.atm_location_confirmation)
        data = await state.get_data()
        addr_data: AddressData = data['address_data']
        await message.answer(
            f"Мы нашли следующую информацию об интересующем вас местоположении банкомата:\n"
            f"\n"
            f"<code>"
            f"Координаты: {addr_data.lat}, {addr_data.lon}\n"
            f"Адрес: {addr_data.address}\n"
            f"</code>"
            f"\n"
            f"Пожалуйста, подтвердите, что данные корректны. Или введите данные заново.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=t) for t in ("1. Данные корректны",
                                                            "2. Хочу ввести данные заново")]],
                resize_keyboard=True)
        )

    @staticmethod
    @router.message(StateFilter(States.atm_location_confirmation), F.text.startswith("1."))
    async def confirm_data(message: types.Message, state: FSMContext):
        await AtmGroupInputStep.init(message, state)

    @staticmethod
    @router.message(StateFilter(States.atm_location_confirmation), F.text.startswith("2."))
    async def repeat_input(message: types.Message, state: FSMContext):
        await AtmDataInputStep.init(message, state)

    @staticmethod
    @router.message(StateFilter(States.atm_location_confirmation))
    async def incorrect_input(message: types.Message):
        await message.reply("Пожалуйста, выберите один из предложенных в меню вариантов действия")


class AtmGroupInputStep:
    atm_groups = None

    @staticmethod
    def get_atm_groups():
        if AtmGroupInputStep.atm_groups is None:
            AtmGroupInputStep.atm_groups = PredictionServiceAdapter.get_atm_groups()
        return AtmGroupInputStep.atm_groups

    @staticmethod
    async def init(message: types.Message, state: FSMContext):
        await state.set_state(States.atm_group_input)
        builder = ReplyKeyboardBuilder()
        for gr in AtmGroupInputStep.get_atm_groups():
            builder.add(types.KeyboardButton(text=gr))
        builder.adjust(4)

        await message.reply("Выберите банковскую группу, банкомат которой планируется разместить:",
                            reply_markup=builder.as_markup(resize_keyboard=True))

    @staticmethod
    @router.message(StateFilter(States.atm_group_input))
    async def input_atm_group(message: types.Message, state: FSMContext):
        if message.text in AtmGroupInputStep.get_atm_groups():
            await state.update_data(atm_group=message.text)
            await ResultViewStep.init(message, state)
        else:
            await message.reply('Пожалуйста, выберите одну из предложенных групп')


class ResultViewStep:
    @staticmethod
    async def init(message: types.Message, state: FSMContext):
        await state.set_state(States.result_view)

        data = await state.get_data()
        addr_data: AddressData = data['address_data']
        atm_group = data['atm_group']

        prediction = PredictionServiceAdapter.predict_one(
            AtmData(
                lat=addr_data.lat,
                lon=addr_data.lon,
                atm_group=atm_group)
        )

        await message.answer(
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
            f"Хотите получить предсказание для еще одного банкомата?\n",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=t) for t in ("1. Еще одно предсказание", "2. Вернуться к началу")]],
                resize_keyboard=True)
        )

    @staticmethod
    @router.message(StateFilter(States.result_view), F.text.startswith("1."))
    async def input_new_atm_data(message: Message, state: FSMContext):
        await AtmDataInputStep.init(message, state)

    @staticmethod
    @router.message(StateFilter(States.result_view), F.text.startswith("2."))
    async def restart_bot(message: Message, state: FSMContext):
        await show_start_message(message, state)
