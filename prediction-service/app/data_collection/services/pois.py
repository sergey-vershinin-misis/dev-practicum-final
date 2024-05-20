from collections import Counter
from pathlib import Path

import geopandas as gpd
import pyrosm
from cartopy.geodesic import Geodesic
from shapely.geometry import Polygon

from ..schemas import OSM_TAGS


tags_filter = {
    "amenity": True,
    "shop": True,
    "leisure": True,
    "office": True,
    "public_transport": True,
    "tourism": True,
}


def load_osm_pbf_to_dataframe(file_path: Path = None) -> gpd.GeoDataFrame:
    # TODO: Temporarily loading only Moscow. Finalize
    # osm = pyrosm.OSM(str(file_path))
    fp = pyrosm.get_data("Moscow")
    osm = pyrosm.OSM(fp)
    # TODO: drop prints and add logging
    print("File loaded")
    main_gpdf = osm.get_pois(
        custom_filter=tags_filter
    )
    print("Dataframe created")
    main_gpdf = main_gpdf.copy()  # Дефрагментация датафрейма
    print("Dataframe defragmentation done")
    return main_gpdf


def get_poi_counts_near_geolocation(
        gdf: gpd.GeoDataFrame,
        lat: float,
        long: float,
        searching_radius: int,  # meters
) -> dict[str, dict]:
    gd = Geodesic()
    circle_polygon = Polygon(gd.circle(lon=long, lat=lat, radius=searching_radius))

    # Быстрая фильтрация предварительных результатов с использованием R-tree index
    spatial_index = gdf.sindex
    possible_matches_index = list(spatial_index.intersection(circle_polygon.bounds))
    possible_matches = gdf.iloc[possible_matches_index]

    # Подробная фильтрация
    gdf_selection = possible_matches[possible_matches.intersects(circle_polygon)]

    tags_count_by_types = {}
    for tag_type in tags_filter.keys():
        tags_count_by_types[tag_type] = dict(gdf_selection.loc[:, tag_type].value_counts())
    return tags_count_by_types


def convert_poi_tag_counts_to_category_counts(pois_in: dict[str, dict]) -> dict:
    counter = Counter()
    for key in pois_in.keys():
        for tag in pois_in[key].keys():
            tag_info = OSM_TAGS.get(tag)
            if tag_info is None:
                continue
            category = tag_info["category"]
            counter[category] += pois_in[key][tag]
    return dict(counter)
