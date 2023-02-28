from typing import Optional

from pydantic import BaseSettings

from web.config.settings.environment import Environment


class WebAppBaseSettings(BaseSettings):
    DEBUG: bool = False
    RELOAD: bool = False

    SERVER_HOST: str = None
    SERVER_PORT: int = None
    SERVER_WORKERS: int = None

    API_PREFIX: str = '/api/v1'

    DATABASE_NAME: str = None

    ENVIRONMENT: Optional[Environment] = None
