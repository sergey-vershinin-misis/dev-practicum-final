import argparse

parser = argparse.ArgumentParser(
    prog='python main.py',
    description='Бот для взаимодействия с сервисом предсказания популярности банкоматов',
    usage='python main.py [аргументы]',
)

parser.add_argument(
    '--atm_project_prediction_service_url',
    type=str,
    help='URL сервиса предсказания',
    metavar='<prediction service url>',
    )

parser.add_argument(
    '--atm_project_bot_token',
    type=str,
    help='токен телеграм-бота',
    metavar='<bot token>',
    )

parser.add_argument(
    '--atm_project_team_chat_id',
    type=str,
    help='ид телеграм-чата проекта (для отправки отзывов)',
    metavar='<chat id>',
)

parser.add_argument(
    '--dadata_api_key',
    type=str,
    help='ключ доступа к API сервиса Dadata',
    metavar='<dadata api key>',
)
