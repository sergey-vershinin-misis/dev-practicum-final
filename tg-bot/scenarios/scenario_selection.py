from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()


@router.message(Command("start"))
async def show_start_message(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f'Здравствуйте, {message.from_user.full_name}!\n'
        f'\n'
        f'С помощью данного бота вы можете получать предсказания индекса популярности '
        f'банкомата на основе данных о его местоположении.\n'
        f'\n'
        f'Для взаимодействия с ботом вы можете использовать следующие команды:\n'
        f'/manual_input - интерактивный ввод данных о банкомате и предсказание индекса популярности\n'
        f'/upload_csv - загрузка CSV-файла с данными о банкоматах и получение файла, дополненного предсказаниями\n'
        f'/model_info - просмотр основной информации об используемой модели предсказания\n'
        f'/send_review - отправка отзыва о работе бота команде разработчиков\n'
        f'/play - игра в "угадай число"',
        reply_markup=ReplyKeyboardRemove()
    )
