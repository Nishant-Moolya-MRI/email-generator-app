from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"

class Settings(BaseSettings):
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    MAIL_MCP_SERVER_URL: str

    model_config = SettingsConfigDict(env_file=ENV_FILE)

settings = Settings()