""" Configuration utils """
import secrets
import warnings
from typing import Annotated, Any, Literal
from pydantic import EmailStr

from pydantic import (
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    PostgresDsn,
    UrlConstraints,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl, Url
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self

# Define a Pydantic definition for SQLite
SQLiteDsn = Annotated[
        Url,
        UrlConstraints(
            host_required=False,
            allowed_schemes=[
                'sqlite',
            ],
        ),
    ]


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    @computed_field  # type: ignore[misc]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    PROJECT_NAME: str = "BOOK-NET"
    SENTRY_DSN: HttpUrl | None = None
    DB_ENGINE: str = "sqlite"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "es_db_user"
    DB_PASSWORD: str | None = None
    DB_NAME: str | None = None

    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn | SQLiteDsn:
        database_uri = None
        # Check database engine
        if self.DB_ENGINE == 'postgres':
            if self.DB_NAME is None:
                self.DB_NAME = 'es_db'
            database_uri = MultiHostUrl.build(
                scheme="postgresql+psycopg",
                username=self.DB_USER,
                password=self.DB_PASSWORD,
                host=self.DB_HOST,
                port=self.DB_PORT,
                path=self.DB_NAME,
            )
        elif self.DB_ENGINE == 'sqlite':
            if self.DB_NAME is None:
                self.DB_NAME = 'es_db.sqlite'
            database_uri = MultiHostUrl.build(
                scheme="sqlite",
                host='',
                path=self.DB_NAME,
            )
        else:
            raise ValueError(f'Invalid database engine {self.DB_ENGINE}. Valid options are [sqlite, postgres]')
        return database_uri

    SMTP_TLS: bool = False
    SMTP_SSL: bool = False
    SMTP_PORT: int = 1025
    SMTP_HOST: str | None = "localhost"
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: Annotated[str, EmailStr] | None = "bookNet@gmail.com"
    EMAILS_FROM_NAME: str | None = "BOOK-NET"

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    @computed_field  # type: ignore[misc]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    EMAIL_TEST_USER: Annotated[str, EmailStr] = "test@example.com"
    FIRST_SUPERUSER: Annotated[str, EmailStr]
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        if self.DB_ENGINE != 'sqlite':
            self._check_default_secret("DB_PASSWORD", self.DB_PASSWORD)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )

        return self
