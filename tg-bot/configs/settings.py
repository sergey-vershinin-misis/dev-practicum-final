from pydantic_settings import BaseSettings
from configs.argparser import parser


class Settings(BaseSettings):
    atm_project_prediction_service_url: str
    atm_project_bot_token: str
    atm_project_team_chat_id: str
    dadata_api_key: str

    def __init__(self, **values):
        super().__init__(**values)
        self.update_with_command_line_args()

    def update_with_command_line_args(self):
        for param_name, param_value in vars(parser.parse_args()).items():
            if param_value is not None:
                setattr(self, param_name, param_value)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
