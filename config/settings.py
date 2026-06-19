from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    db_type: str = Field(default="sqlite", validation_alias="DB_TYPE")
    sqlite_db_path: str = Field(
        default="snippets.db", validation_alias="SQLITE_DB_PATH"
    )

    mysql_host: str = Field(default="localhost", validation_alias="MYSQL_HOST")
    mysql_port: int = Field(default=3306, validation_alias="MYSQL_PORT")
    mysql_database: str = Field(
        default="snippet_vault", validation_alias="MYSQL_DATABASE"
    )
    mysql_user: str = Field(default="mysql_user", validation_alias="MYSQL_USER")
    mysql_password: str = Field(
        default="mysql_password", validation_alias="MYSQL_PASSWORD"
    )
    mysql_root_password: str = Field(
        default="mysql_root_password", validation_alias="MYSQL_ROOT_PASSWORD"
    )

    @field_validator("db_type", mode="before")
    @classmethod
    def clean_db_type(cls, v):
        if not v or not isinstance(v, str):
            return "sqlite"
        return v.strip().lower()

    @field_validator("mysql_port", mode="before")
    @classmethod
    def parse_mysql_port(cls, v):
        if v is None or (isinstance(v, str) and v.strip() == ""):
            return 3306
        try:
            return int(v)
        except ValueError:
            return 3306

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
