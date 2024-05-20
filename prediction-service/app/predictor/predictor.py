import math
import pickle

import numpy as np
import pandas as pd
from sklearn.ensemble import StackingRegressor
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

from app.configs import Settings
from app.data_collection import (
    extend_original_atm_dataset,
    load_osm_pbf_to_dataframe,
)
from app.dto_models import AtmData

REQUIRED_FEATURE_LIST = ['atm_group', 'lat', 'long', 'city', 'federal_district', 'region_with_type', 'locality_area',
                         'locality_population', 'sustenance', 'education', 'fuel', 'car_service', 'parking_space',
                         'atm',
                         'bank', 'bureau_de_change', 'outpatient_medical_facilities', 'inplace_medical_facilities',
                         'pharmacy', 'veterinary', 'entertainment', 'entertainment_for_adults',
                         'administrative_buildings', 'police', 'fire_station', 'post_office', 'grave_yard',
                         'marketplace', 'monastery', 'place_of_worship', 'public_transport_stop_position',
                         'alcohol_shop', 'food_shop', 'supermarket', 'mall', 'wholesale', 'clothing_shop',
                         'discount_store', 'beauty_store', 'hardware_store', 'interior_store', 'electronics_store',
                         'sport_store', 'auto_moto_store', 'car_parts_store', 'hobbies_store', 'books_store', 'hotel',
                         'museum']

ATM_GROUPS = ['Rosbank', 'AkBars', 'Alfabank', 'Gazprombank', 'Raiffeisen', 'Rosselkhozbank', 'Uralsib']


class Predictor:
    def __init__(self, settings: Settings):
        self.__settings = settings
        self._load_components()

    def _load_components(self):
        if self.__settings.data_enrichment_enabled:
            print("Start loading osm dataframe")
            self.osm_gdf = load_osm_pbf_to_dataframe()
            print("Osm dataframe successfully loaded")
        else:
            print("Data enrichment disabled (DATA_ENRICHMENT_ENABLED env variable is set to False)")

        with open("app/predictor/Imputer.pickle", "rb") as f:
            self.imputer: SimpleImputer = pickle.load(f)
        with open("app/predictor/Encoder.pickle", "rb") as f:
            self.encoder: OneHotEncoder = pickle.load(f)
        with open("app/predictor/Scaler.pickle", "rb") as f:
            self.scaler: StandardScaler = pickle.load(f)
        with open("app/predictor/Model.pickle", "rb") as f:
            self.model: StackingRegressor = pickle.load(f)

    def predict(self, atm_data_list: list[AtmData]) -> list[float]:
        df = self.__enrich_data(atm_data_list)

        df = self.__preprocess_data(df)

        return self.model.predict(df).tolist()

    def enrich(self, atm_data_list: list[AtmData]) -> list[dict]:
        results = self.__enrich_data(atm_data_list).to_dict('records')
        for result in results:
            for key, value in result.items():
                if (value == np.NaN) or (isinstance(value, float) and math.isnan(value)):
                    result[key] = None
        return results

    def __enrich_data(self, atm_data_list: list[AtmData]) -> pd.DataFrame:
        if self.__settings.data_enrichment_enabled:
            df = extend_original_atm_dataset(
                dataset=atm_data_list,
                dadata_api_key=self.__settings.dadata_api_key,
                dadata_secret=self.__settings.dadata_secret_key,
                geo_tree_api_key=self.__settings.geo_tree_secret_key,
                osm_dataframe=self.osm_gdf,
                searching_radius=self.__settings.pois_searching_radius,
            )
        else:
            df = pd.DataFrame(dict(item) for item in atm_data_list)

        df = self.__adjust_columns(df)
        self.__assert_feature_presence_and_order(df)
        return df

    def __adjust_columns(self, df):
        # меняем lon на long, т.к. в датасете оно long
        if "lon" in df.columns:
            df.rename(columns={"lon": "long"}, inplace=True)

        # создаем недостающие столбцы и заполняем их NaN, чтобы потом их заполнил Imputer
        for col in REQUIRED_FEATURE_LIST:
            if col not in df.columns:
                df[col] = np.NaN

        # возвращаем датафрейм, но с тем порядком столбцов, который задан в требованиях
        return df[REQUIRED_FEATURE_LIST]

    def __assert_feature_presence_and_order(self, df: pd.DataFrame) -> None:
        assert df.columns.tolist() == REQUIRED_FEATURE_LIST

    def __preprocess_data(self, df):
        # заполняем пропуски
        df[df.columns] = self.imputer.transform(df)

        # кодируем категориальные признаки
        cat_cols = ['atm_group', 'federal_district', 'city', 'region_with_type']
        encoded_columns_df = pd.DataFrame(self.encoder.transform(df[cat_cols]).toarray(),
                                          columns=self.encoder.get_feature_names_out(cat_cols),
                                          dtype=int)
        df = pd.concat(
            [
                df.drop(columns=cat_cols).reset_index(drop=True),
                encoded_columns_df.reset_index(drop=True)
            ],
            axis=1
        )

        # масштабируем признаки
        df = pd.DataFrame(self.scaler.transform(df), columns=df.columns)
        return df
