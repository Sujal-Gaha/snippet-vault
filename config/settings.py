from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    sqlite_db_path: str = Field(
        default="snippets.db", validation_alias="SQLITE_DB_PATH"
    )

    @field_validator("sqlite_db_path", mode="before")
    @classmethod
    def parse_sqlite_path(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ""):
            return "snippets.db"
        return v.strip()


class StreamlitSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    server_port: int = Field(default=1234, validation_alias="STREAMLIT_SERVER_PORT")
    server_address: str = Field(
        default="0.0.0.0", validation_alias="STREAMLIT_SERVER_ADDRESS"
    )

    @field_validator("server_port", mode="before")
    @classmethod
    def parse_server_port(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ""):
            return 1234
        try:
            return int(v)
        except ValueError:
            return 1234


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    db: DatabaseSettings = DatabaseSettings()
    streamlit: StreamlitSettings = StreamlitSettings()


# Global settings instance
settings = Settings()
