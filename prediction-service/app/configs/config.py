from pydantic_settings import BaseSettings

from app.configs.argparser import parser


class Settings(BaseSettings):
    port: int = 80

    dadata_api_key: str
    dadata_secret_key: str
    geo_tree_secret_key: str

    data_enrichment_enabled: bool = True
    redis_host: str = "localhost"
    redis_port: str = "6379"

    datasets_dir_path: str = "datasets"
    initial_dataset_name: str = "train_initial.csv"
    fixed_dataset_name: str = "train_initial_fixed.csv"
    with_geodata_dataset_name: str = "train_with_geo_data.csv"
    extended_with_pois_dataset_name: str = "train_with_pois.csv"

    data_dir_path: str = "data"
    osm_cache_filename: str = "filtered-russia-06-11.osm.pbf"

    pois_searching_radius: int = 150

    def __init__(self, **values):
        super().__init__(**values)
        self.update_with_command_line_args()

    def update_with_command_line_args(self):
        for param_name, param_value in vars(parser.parse_args()).items():
            if param_value is not None:
                setattr(self, param_name, param_value)

    class Config:
        env_file = "app/.env"
        env_file_encoding = "utf-8"
