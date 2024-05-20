import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from scenarios import (
    scenario_selection,
    upload_csv_with_atm_data,
    manual_atm_data_input,
    show_model_info,
    send_review,
    play_game,
    process_unknown
)
from configs.settings import settings


dp = Dispatcher()
dp.include_routers(
    scenario_selection.router,
    manual_atm_data_input.router,
    upload_csv_with_atm_data.router,
    show_model_info.router,
    send_review.router,
    play_game.router,
    process_unknown.router,
)


async def main() -> None:
    bot = Bot(settings.atm_project_bot_token, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
