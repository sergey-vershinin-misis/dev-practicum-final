import csv
import io
import os
from contextlib import asynccontextmanager
from tempfile import NamedTemporaryFile
from typing import List

import pandas as pd
from fastapi import FastAPI
from fastapi import UploadFile
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import Redis
from starlette.background import BackgroundTask
from starlette.responses import FileResponse

from app.configs import Settings
from app.dto_models import AtmData
from app.predictor.predictor import Predictor, ATM_GROUPS

settings = Settings()
predictor = Predictor(settings)


#
@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = Redis(host=settings.redis_host, port=settings.redis_port, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/atm-groups")
@cache(expire=300)
def get_atm_groups() -> List[str]:
    """Возвращает перечень банковских групп"""
    return ATM_GROUPS


@app.get("/health")
async def healthcheck():
    return {"status": "alive"}


@app.post("/predict-one")
# @cache(expire=300)
# к сожалению, fastapi-cache не умеет корректно формировать ключ по объекту pydantic-модели
# изучение документации и поиск в интернете за разумное время не привел к решению (например, фрагменты
# кода с кастомным key-генератором с их github - нерабочие). В связи с этим кэширование
# пришлось оставить только для ручки выше. А здесь и ниже кеширование пока закомментировано
def predict_one(atm_data: AtmData) -> float:
    """Предсказывает индекс популярности для одного банкомата"""
    return predictor.predict([atm_data])[0]


@app.post("/predict-many")
# @cache(expire=300)
def predict_many(atm_data_list: List[AtmData]) -> List[float]:
    """Предсказывает индекс популярности для нескольких банкоматов"""
    return predictor.predict(atm_data_list)


@app.post('/predict-csv')
def predict_csv(file: UploadFile) -> FileResponse:
    """Предсказывает индекс популярности банкоматов, данные о которых были переданы в виде CSV-файла. Результат
    возвращает в виде дополненного прогнозными значениями CSV-файлв"""
    items: List[AtmData] = []
    with file.file as f:
        reader = csv.DictReader(io.TextIOWrapper(f))
        for row in reader:
            items.append(AtmData.model_validate(row))

    df = pd.DataFrame(dict(item) for item in items)
    df['target'] = predictor.predict(items)

    f = NamedTemporaryFile(delete=False)
    df.to_csv(f, index=False)

    return FileResponse(
        path=f.name,
        media_type='text/csv',
        filename='results.csv',
        background=BackgroundTask(os.remove, f.name)
    )


@app.post("/enrich-many")
# @cache(expire=300)
def enrich_many(atm_data_list: List[AtmData]):
    """Обогащает исходные данные о банкоматах дополнительными параметрами, такими как площадь и
     численность населения, количество школ, остановок, магазинов и т.п. в окрестности и прочее.
     В связи с тех.ограничениями на данный момент работает только для города Москва"""
    """"""
    return predictor.enrich(atm_data_list)
