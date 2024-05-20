import json
import requests
from pydantic import BaseModel

from configs.settings import settings


class AtmData(BaseModel):
    lat: float
    lon: float
    atm_group: str


HEADERS = {'Content-type': 'application/json', 'accept': 'application/json'}


class PredictionServiceAdapter:

    @staticmethod
    def predict(atm_data):
        return atm_data

    @staticmethod
    def get_atm_groups() -> list[str]:
        response = requests.get(f'{settings.atm_project_prediction_service_url}/atm-groups', headers=HEADERS)
        return response.json()

    @staticmethod
    def predict_one(atm_data: AtmData) -> float | None:

        response = requests.post(
            f'{settings.atm_project_prediction_service_url}/predict-one',
            data=atm_data.model_dump_json().encode('utf8'),
            headers=HEADERS,

        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Prediction service adapter. Error while making request: {response.status_code}, {response.text}')
            return None

    @staticmethod
    def predict_many(atm_data_list: list[AtmData]) -> list[float] | None:

        response = requests.post(
            f'{settings.atm_project_prediction_service_url}/predict-many',
            data=json.dumps([atm_data.model_dump() for atm_data in atm_data_list]),
            headers=HEADERS
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Prediction service adapter. Error while making request: {response.status_code}, {response.text}')
            return None
