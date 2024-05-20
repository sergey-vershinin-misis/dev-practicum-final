from typing import Literal

from dadata import Dadata

from ..exceptions import (
    DadataObjectsNotFound,
    DadataValidationError,
    DadataInvalidParameters,
)
from ..schemas import (
    DadataResponse,
    ExtendedGeoData,
    ExtendedGeoDataExecutionResult,
    OriginalGeoData,
)


def _validate_dadata_geolocation(geolocation: DadataResponse) -> Literal[True]:
    if geolocation.country_iso_code != "RU":
        raise DadataValidationError(
            "Geolocation is outside the Russian Federation"
        )
    return True


def _is_metro_in_geolocation_city(geolocation: DadataResponse) -> bool:
    cities_with_metro_fias_ids = (
        "0c5b2444-70a0-4932-980c-b4dc0d3f02b5"  # Москва
        "c2deb16a-0330-4f05-821f-1d09c93331e6"  # Санкт-Петербург
        "bb035cc3-1dc2-4627-9d25-a1bf2d4b936b"  # Самара
        "555e7d61-d9a7-4ba6-9770-6caa8198c483"  # Нижний Новгород
        "93b3df57-4c89-44df-ac42-96f05e9cd3b9"  # Казань
        "2763c110-cb8b-416a-9dac-ad28a55b4402"  # Екатеринбург
        "8dea00e3-9aab-4d8e-887c-ef2aaa546456"  # Новосибирск
    )
    if geolocation.city_fias_id is None:
        return False
    return geolocation.city_fias_id in cities_with_metro_fias_ids


def _get_nearest_metro_distance(geolocation: DadataResponse) -> float | None:
    if geolocation.metro is None:
        return
    return geolocation.metro[0].distance


def _find_geolocation_by_coordinates_from_dadata(lat: float, long: float,
                                                 dadata_client: Dadata) -> DadataResponse:
    response = dadata_client.geolocate(
        name="address",
        lat=lat,
        lon=long,
    )
    if not response:
        raise DadataObjectsNotFound(
            f"The Dadata service was unable to geolocate the address by lat: {lat}, "
            f"lon: {long}"
        )
    geolocation_obj = DadataResponse.model_validate({
        **response[0]["data"],
        "address_rus": response[0]["unrestricted_value"]
    })
    _validate_dadata_geolocation(geolocation_obj)
    return geolocation_obj


def _find_geolocation_by_address_from_dadata(address: str,
                                             dadata_client: Dadata) -> DadataResponse:
    response = dadata_client.clean(name="address", source=address)
    if response["result"] is None:
        raise DadataObjectsNotFound(
            f"The Dadata service was unable to geolocate the address: {address}"
        )
    geolocation_obj = DadataResponse.model_validate({
        **response,
        "address_rus": response["result"]
    })
    _validate_dadata_geolocation(geolocation_obj)
    return geolocation_obj


def _merge_geolocation_by_coordinates_and_by_address(
        data_by_coordinates: DadataResponse | None,
        data_by_address: DadataResponse | None,
) -> DadataResponse | None:
    if data_by_coordinates is None:
        if data_by_address is None:
            return None
        return data_by_address
    elif data_by_address is None:
        return data_by_coordinates
    first_dict = data_by_coordinates.model_dump()
    second_dict = data_by_address.model_dump()
    result_dict = {key: (first_dict[key] if first_dict[key] is not None
                         else second_dict[key]) for key in first_dict}
    return DadataResponse.model_validate(result_dict)


def get_extended_geo_data_from_dadata(
        geo_in: OriginalGeoData,
        dadata_client: Dadata
) -> ExtendedGeoDataExecutionResult:
    # TODO: add docstring
    geolocation_by_coordinates = None
    geolocation_by_address = None
    distance_to_metro = None
    geocoding_warnings = []
    lat = geo_in.lat
    long = geo_in.long

    if lat and long:
        try:
            geolocation_by_coordinates = _find_geolocation_by_coordinates_from_dadata(
                lat=geo_in.lat, long=geo_in.long, dadata_client=dadata_client,
            )
        except (DadataObjectsNotFound, DadataValidationError) as exc:
            geocoding_warnings.append(str(exc))

    if geolocation_by_coordinates is None:
        address = geo_in.address_rus or geo_in.address
        if not address:
            raise DadataInvalidParameters(
                "No geolocation data available. No coordinates or address."
            )
        geolocation_by_address = _find_geolocation_by_address_from_dadata(
            address=geo_in.address,
            dadata_client=dadata_client
        )
        distance_to_metro = _get_nearest_metro_distance(geolocation_by_address)
        lat = geolocation_by_address.geo_lat
        long = geolocation_by_address.geo_lon

    elif _is_metro_in_geolocation_city(geolocation_by_coordinates):
        try:
            geolocation_by_address = _find_geolocation_by_address_from_dadata(
                address=geolocation_by_coordinates.address_rus,
                dadata_client=dadata_client,
            )
            distance_to_metro = _get_nearest_metro_distance(geolocation_by_address)
        except (DadataObjectsNotFound, DadataValidationError) as exc:
            geocoding_warnings.append(str(exc))

    geolocation = _merge_geolocation_by_coordinates_and_by_address(
        geolocation_by_coordinates, geolocation_by_address,
    )

    geo_out = ExtendedGeoData.model_validate({
        "lat": lat,
        "long": long,
        "address": geo_in.address,
        "address_rus": geo_in.address_rus or geolocation.address_rus,
        "city": geolocation.city_with_type or geolocation.settlement_with_type,
        "oktmo": geolocation.oktmo,
        "city_area": geolocation.city_area,
        "city_district": geolocation.city_district_with_type,
        "metro": distance_to_metro,
        "federal_district": geolocation.federal_district,
        "region_with_type": geolocation.region_with_type,
        "capital_marker": geolocation.capital_marker,
    })

    return ExtendedGeoDataExecutionResult.model_validate({
        "geolocation": geo_out,
        "warnings": geocoding_warnings
    })
