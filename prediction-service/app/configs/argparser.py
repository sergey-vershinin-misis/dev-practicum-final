import argparse

parser = argparse.ArgumentParser(
    prog='python main.py',
    description='web-сервис для предсказания популярности банкоматов',
    usage='python main.py [аргументы]',
)

parser.add_argument(
    '--port',
    type=int,
    help='порт для запуска сервиса',
    metavar='<service port>',
    )

parser.add_argument(
    '--data_enrichment_enabled',
    type=bool,
    action=argparse.BooleanOptionalAction,
    help='определяет, нужно ли обогащать данные с помощью внешних сервисов',
)

parser.add_argument(
    '--redis_host',
    type=str,
    help='адрес хоста, на котором запущен redis',
    metavar='<redis host>',
    )

parser.add_argument(
    '--redis_port',
    type=str,
    help='порт, на котором запущен redis',
    metavar='<redis port>',
    )

parser.add_argument(
    '--dadata_api_key',
    type=str,
    help='api-ключ сервиса Dadata',
    metavar='<dadata api key>',
    )

parser.add_argument(
    '--dadata_secret_key',
    type=str,
    help='api-ключ сервиса Dadata',
    metavar='<dadata secret key>',
    )

parser.add_argument(
    '--geo_tree_secret_key',
    type=str,
    help='api-ключ сервиса GeoTree',
    metavar='<geotree secret key>',
    )

