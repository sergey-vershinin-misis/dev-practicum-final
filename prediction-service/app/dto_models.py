from pydantic import BaseModel


class AtmData(BaseModel):
    """Исходные данные о банкомате, необходимые для прогнозирования индекса
    популярности"""
    lat: float
    lon: float
    atm_group: str
