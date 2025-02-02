# Сервис прогнозирования индекса популярности места для размещения банкомата

## Оглавление
- [назначение сервиса прогнозирования](#назначение)
- [компоненты в составе сервиса](#компоненты-сервиса)
- [запуск компонент сервиса](#запуск-компонент-сервиса)
- [статический контроль кода](#контроль-кода-с-помощью-flake8)
- [автоматические тесты](#автоматические-тесты)
- [CI/CD-pipeline](#сicd-pipeline-публикации-docker-образов-на-docker-hub)
- [команда проекта](#состав-команды)

## Назначение
Сервис предназначен для прогнозирования индекса популярности мест для размещения банкоматов. Для взаимодействия с сервисом создан Telegram-бот, предоставляющий пользователю возможность указать место размещения банкомата с помощью координат или адреса, либо просто загрузить CSV-файл с координатами сразу нескольких банкоматов, после чего получить результаты прогнозирования в виде текста или дополненного прогнозами CSV-файла. 

## Компоненты сервиса
В состав сервиса входят следующие компоненты: 
- Telegram-бот для взаимодействия с сервисом (_подробное описание функциональных возможностей бота, а также его внутренней организации [приведено на отдельной странице](tg-bot/README.md)_);  
- web-сервис, реализованный с помощью библиотеки FastAPI и выполняющий обогащение введенных пользователем параметров данными сторонних сервисов и последующее прогнозирование индекса популярности банкомата в указанном месте (_подробное описание api сервиса и его внутренней организации [приведено на странице с описанием сервиса прогнозирования](prediction-service/README.md)_).


## Запуск компонент сервиса
### Запуск с помощью ```docker compose```
Наиболее простым способом запуска компонентов сервиса является использование находящегося ```docker compose```. Для этого скачайте расположенный в репозитории файл [docker-compose.yml](docker-compose.yml), а также [.env-template](.env-template), после чего переименуйте последний в _.env_ и укажите в нем реальные параметры запуска telegram-бота и доступа к внешним сервисам. 

После выполнения указанных действий просто выполните команду ```docker compose up -d``` и начните чат с telegram-ботом, чей токен вы указали в .env-файле.  

### Запуск без использования docker
Чтобы запустить компоненты сервисы без использования docker вам необходимо выполнить следующую последовательность действий: 

- разверните _Redis_, которые необходим для кэширования запросов к web-сервису, и получите параметры доступа к нему;
- запустите web-сервис; для этого сохраните локально содержимое каталога [prediction-service](prediction-service/) и выполните следующую команду:
```python
python main.py
  --port=<порт, на котором будет запущен сервис>
  --redis_host=<хост, где размещен redis>
  --redis_port=<порт, на котором запущен redis> 
  --data_enrichment_enabled (или --no-data_enrichment_enabled)
  --dadata_api_key=<api-ключ к сервису Dadata.ru>
  --dadata_secret_key=<secret-ключ к сервису Dadata.ru>
  --geo_tree_secret_key=<secret-ключ к сервису GeoTree.ru>
```   
- после успешного запуска web-сервиса запустите Telegram-бот; для этого сохраните локально содержимое каталога [tg-bot](tg-bot/) и выполните следующую команду:
```python
python main.py
  --atm_project_prediction_service_url=<URI web-сервиса предсказаний>
  --atm_project_bot_token=<токен telegram-бота>
  --atm_project_team_chat_id=<id чата, в который будут отправляться отзывы> 
  --dadata_api_key=<api-ключ к сервису Dadata.ru>
```   

Состав доступных параметров командной строки можно также получить с использованием команды ```python main.py --help```

Обратите внимание, что в случае, когда параметр _data_enrichment_enabled_, определяющий, требуется ли обогащение данных из внешних источников, установлен в _True_, запуск web-сервиса может занимать несколько минут, что связано с загрузкой и предобработкой базы данных OpenStreetMap.

## Контроль кода (с помощью flake8)
Для контроля качества кода компонентов сервиса использована библиотека flake8 со стандартными настройками (за исключением измененной на 120
длины строки)

## Автоматические тесты
Для telegram-бота с использованием библиотек _pytest_ и _unittest.mock_  реализован набор автоматических тестов. Подробное описание состава тестов приведено на [отдельной странице описания бота](tg-bot/README.md).