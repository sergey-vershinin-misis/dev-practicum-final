import csv
import pathlib

from ..schemas import (
    FilteredGeoData,
    OriginalDatasetObject,
    PopulationStats,
)


def load_dataset_from_csv(filename: pathlib.Path) -> list[dict]:
    dataset = []
    with open(filename) as file:
        reader = csv.DictReader(file)
        for row in reader:
            dataset.append(row)
    return dataset


def save_dataset_to_csv(filename: pathlib.Path, dataset: list[dict]) -> None:
    with open(filename, "w") as file:
        field_names = tuple(dataset[0].keys())
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        for entry in dataset:
            writer.writerow(entry)


def merge_original_atm_dataset_with_extended_data(
        initial_dataset_obj: OriginalDatasetObject,
        geolocation: FilteredGeoData | None,
        population_stats: PopulationStats | None,
        pois_obj: dict | None
) -> dict:
    if geolocation is None:
        geolocation = FilteredGeoData()
    if population_stats is None:
        population_stats = PopulationStats()
    if pois_obj is None:
        pois_obj = {}
    return {
        **initial_dataset_obj.model_dump(),
        **geolocation.model_dump(),
        **population_stats.model_dump(),
        **pois_obj,
    }
