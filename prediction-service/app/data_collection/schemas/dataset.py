from pydantic import BaseModel, Field, field_validator


def _empty_str_to_none(value):
    if value == "":
        return None
    return value


class GeoCoordinatesBase(BaseModel):
    lat: float | None = Field(default=None)
    long: float | None = Field(default=None)

    @field_validator("lat", "long", mode="before")
    def check_empty_string(cls, value):
        return _empty_str_to_none(value)


class OriginalDatasetObject(GeoCoordinatesBase):
    atm_group: str = Field(...)
    address: str | None = Field(default=None)
    address_rus: str | None = Field(default=None)


class OriginalGeoData(GeoCoordinatesBase):
    address: str | None = Field(default=None)
    address_rus: str | None = Field(default=None)


class ExtendedGeoData(OriginalGeoData):
    city: str | None = Field(default=None)
    oktmo: str | None = Field(default=None)
    city_area: str | None = Field(default=None)
    city_district: str | None = Field(default=None)
    metro: float | None = Field(default=None)
    federal_district: str | None = Field(default=None)
    region_with_type: str | None = Field(default=None)
    capital_marker: str | None = Field(default=None)


class FilteredGeoData(OriginalGeoData):
    city: str | None = Field(default=None)
    city_area: str | None = Field(default=None)
    city_district: str | None = Field(default=None)
    metro: float | None = Field(default=None)
    federal_district: str | None = Field(default=None)
    region_with_type: str | None = Field(default=None)
    capital_marker: str | None = Field(default=None)


class DatasetObjectWithGeoData(OriginalDatasetObject, ExtendedGeoData):
    ...


class ExtendedGeoDataExecutionResult(BaseModel):
    geolocation: ExtendedGeoData = Field(...)
    warnings: list[str] = Field(...)


class PopulationStats(BaseModel):
    locality_area: float | None = Field(default=None)
    locality_population: float | None = Field(default=None)


class PopulationStatsExecutionResults(BaseModel):
    population_stats: dict[str, PopulationStats] = Field(...)
    exceptions: list[dict] = Field(...)


class MetroOut(BaseModel):
    name: str = Field(...)
    line: str = Field(...)
    distance: float = Field(...)


class DadataResponse(BaseModel):
    city_with_type: str | None = Field(default=None)
    city_area: str | None = Field(default=None)
    city_district_with_type: str | None = Field(default=None)
    city_fias_id: str | None = Field(default=None)
    oktmo: str | None = Field(default=None)
    country_iso_code: str | None = Field(default=None)
    geo_lat: float | None = Field(default=None)
    geo_lon: float | None = Field(default=None)
    metro: list[MetroOut] | None = Field(default=None)
    settlement_with_type: str | None = Field(default=None)
    address_rus: str | None = Field(default=None)
    federal_district: str | None = Field(default=None)
    region_with_type: str | None = Field(default=None)
    capital_marker: str | None = Field(default=None)

    @field_validator("geo_lat", "geo_lon", mode="before")
    def string_to_float(cls, value):
        if isinstance(value, str) and value.isnumeric():
            return float(value)
        return value
