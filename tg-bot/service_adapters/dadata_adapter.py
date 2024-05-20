from dataclasses import dataclass
from dadata import Dadata
from configs.settings import settings


@dataclass
class AddressData:
    lat: float
    lon: float
    address: str
    qc_geo: int


class DadataAdapter:
    @staticmethod
    def get_data_by_address(query: str) -> AddressData | None:
        dadata = Dadata(settings.dadata_api_key)
        res = dadata.suggest("address", query, count=1)
        return DadataAdapter.extract_addr_data(res)

    @staticmethod
    def get_data_by_coords(lat: float, lon: float) -> AddressData | None:
        dadata = Dadata(settings.dadata_api_key)
        res = dadata.geolocate(name="address", lat=lat, lon=lon)
        return DadataAdapter.extract_addr_data(res)

    @staticmethod
    def extract_addr_data(query_result):
        if (query_result is None) or (len(query_result) < 1):
            return None
        result = query_result[0]
        return AddressData(
            address=result.get('unrestricted_value'),
            lat=float(result['data'].get('geo_lat')),
            lon=float(result['data'].get('geo_lon')),
            qc_geo=int(result['data'].get('qc_geo'))
        )
