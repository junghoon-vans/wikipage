from typing import List
from typing import Optional

from pydantic import AnyHttpUrl
from pydantic import field_validator
from pydantic import PostgresDsn
from pydantic import ValidationInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] | str = []

    @field_validator("BACKEND_CORS_ORIGINS", mode='before')
    @classmethod
    def assemble_cors_origins(cls, v: Optional[str])\
            -> Optional[List[AnyHttpUrl]] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode='before')
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo)\
            -> Optional[PostgresDsn]:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_SERVER"),
            path=f"{info.data.get('POSTGRES_DB') or ''}",
        )

    ELASTICSEARCH_HOSTS: str


settings = Settings()
