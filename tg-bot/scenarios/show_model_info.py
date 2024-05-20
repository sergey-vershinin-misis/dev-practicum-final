import time

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile

from scenarios.scenario_selection import show_start_message

router = Router()


@router.message(Command("model_info"))
async def show_model_info(message: Message, state: FSMContext):
    with open("img/model_info.png", "rb") as image_from_buffer:
        await message.answer_photo(
            BufferedInputFile(
                image_from_buffer.read(),
                filename="model_info.png"
            ),
            caption="Мы еще работаем над поиском лучшей модели предсказаний, поэтому информация будем уточняться. А "
                    "пока мы используем для предсказаний модель линейной регрессии, реализованной в классе Lasso() "
                    "библиотеки scikit-learn."
                    "\n\n"
                    "Перед прогнозированием значения индекса популярности банкомата мы дополняем введенные вами "
                    "данные информацией о составных частях адреса, численности и площади населенного пункта, а также "
                    "числом различных объектов, находящихся поблизости от выбранного вами местоположения."
                    "\n\n"
                    "На изображении выше приведена SHAP-диаграмма, отображающая значимость используемых признаков "
                    "с точки зрения текущей модели предсказаний."
        )

    time.sleep(2)
    await show_start_message(message, state)
