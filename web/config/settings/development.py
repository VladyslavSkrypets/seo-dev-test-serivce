from web.config.settings.base import WebAppBaseSettings
from web.config.settings.environment import Environment


class WebAppDevSettings(WebAppBaseSettings):
    DEBUG: bool = True
    RELOAD: bool = True

    SERVER_HOST: str = '127.0.0.1'
    SERVER_PORT: int = 5555
    SERVER_WORKERS: int = 1

    DATABASE_NAME: str = 'test'

    ENVIRONMENT: Environment = Environment.DEVELOPMENT

