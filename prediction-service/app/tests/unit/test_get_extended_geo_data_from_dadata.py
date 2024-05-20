import unittest
from unittest.mock import MagicMock, patch

from app.data_collection.services import get_extended_geo_data_from_dadata
from app.data_collection.exceptions import (
    DadataObjectsNotFound,
    DadataValidationError,
    DadataInvalidParameters,
)
from app.data_collection.schemas import (
    OriginalGeoData,
)


class InputDataMocks:
    @staticmethod
    def get_input_data():
        return OriginalGeoData(
            lat=55.7558,
            long=37.6173,
            address="address",
            address_rus="адрес",
        )


class DadataMocks:
    @staticmethod
    def get_geo_data_by_coordinates_response(lat, lon):
        mock_geo_data = MagicMock(
            geo_lat=lat,
            geo_lon=lon,
            city_with_type="city with type",
            oktmo="oktmo",
            city_area="city area",
            city_district_with_type="city district with type",
            federal_district="federal district",
            region_with_type="region with type",
            capital_marker="capital marker",
        )
        return mock_geo_data

    @staticmethod
    def get_geo_data_by_address_response():
        mock_geo_data = MagicMock(
            geo_lat=55.8558,
            geo_lon=37.7173,
            city_with_type="city with type",
            oktmo="oktmo",
            city_area="city area",
            city_district_with_type="city district with type",
            federal_district="federal district",
            region_with_type="region with type",
            capital_marker="capital marker",
        )
        return mock_geo_data


class TestGetExtendedGeoDataFromDadata(unittest.TestCase):
    @patch("app.data_collection.services.geo_coding._merge_geolocation_by_coordinates_and_by_address")
    @patch("app.data_collection.services.geo_coding._is_metro_in_geolocation_city")
    @patch("app.data_collection.services.geo_coding._get_nearest_metro_distance")
    @patch("app.data_collection.services.geo_coding._find_geolocation_by_address_from_dadata")
    @patch("app.data_collection.services.geo_coding._find_geolocation_by_coordinates_from_dadata")
    def test_successful_geodata_by_coordinates(
            self,
            mock_find_by_coordinates,
            mock_find_by_address,
            mock_find_nearest_metro,
            mock_is_metro_in_geolocation,
            mock_merge_geolocation
    ):
        input_geo_data = InputDataMocks.get_input_data()
        mock_geo_data = DadataMocks.get_geo_data_by_coordinates_response(
            input_geo_data.lat,
            input_geo_data.long,
        )
        mock_find_by_coordinates.return_value = mock_geo_data
        mock_is_metro_in_geolocation.return_value = False
        mock_dadata_client = MagicMock(name="DaDataClientMock")
        mock_merge_geolocation.return_value = mock_geo_data

        result = get_extended_geo_data_from_dadata(
            geo_in=input_geo_data,
            dadata_client=mock_dadata_client,
        )

        mock_find_by_address.assert_not_called()
        mock_find_nearest_metro.assert_not_called()
        mock_find_by_coordinates.assert_called_once_with(
            lat=input_geo_data.lat,
            long=input_geo_data.long,
            dadata_client=mock_dadata_client,
        )
        mock_is_metro_in_geolocation.assert_called_once_with(mock_geo_data)
        mock_merge_geolocation.assert_called_once_with(mock_geo_data, None)

        self.assertEqual(result.geolocation.lat, input_geo_data.lat)
        self.assertEqual(result.geolocation.long, input_geo_data.long)

    @patch("app.data_collection.services.geo_coding._merge_geolocation_by_coordinates_and_by_address")
    @patch("app.data_collection.services.geo_coding._is_metro_in_geolocation_city")
    @patch("app.data_collection.services.geo_coding._get_nearest_metro_distance")
    @patch("app.data_collection.services.geo_coding._find_geolocation_by_address_from_dadata")
    @patch("app.data_collection.services.geo_coding._find_geolocation_by_coordinates_from_dadata")
    def test_successful_geodata_by_address(
            self,
            mock_find_by_coordinates,
            mock_find_by_address,
            mock_find_nearest_metro,
            mock_is_metro_in_geolocation,
            mock_merge_geolocation
    ):
        nearest_metro_distance = 30.5

        input_geo_data = InputDataMocks.get_input_data()
        mock_geo_data_by_address = DadataMocks.get_geo_data_by_address_response()
        mock_find_by_coordinates.return_value = None
        mock_find_by_address.return_value = mock_geo_data_by_address
        mock_find_nearest_metro.return_value = nearest_metro_distance
        mock_dadata_client = MagicMock(name="DaDataClientMock")
        mock_merge_geolocation.return_value = mock_geo_data_by_address

        result = get_extended_geo_data_from_dadata(
            geo_in=input_geo_data,
            dadata_client=mock_dadata_client,
        )

        mock_is_metro_in_geolocation.assert_not_called()
        mock_find_by_coordinates.assert_called_once_with(
            lat=input_geo_data.lat,
            long=input_geo_data.long,
            dadata_client=mock_dadata_client,
        )
        mock_find_by_address.assert_called_once_with(
            address=input_geo_data.address,
            dadata_client=mock_dadata_client,
        )
        mock_find_nearest_metro.assert_called_once_with(mock_geo_data_by_address)
        mock_merge_geolocation(None, mock_geo_data_by_address)

        self.assertEqual(result.geolocation.lat, mock_geo_data_by_address.geo_lat)
        self.assertEqual(result.geolocation.long, mock_geo_data_by_address.geo_lon)
        self.assertEqual(result.geolocation.metro, nearest_metro_distance)


if __name__ == "__main__":
    unittest.main()
