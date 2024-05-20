from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def process_unknown_message(message: Message):
    await message.reply("К сожалению, мы не смогли обработать ваше сообщение. Пожалуйста, используйте одну из "
                        "доступных команд бота")
