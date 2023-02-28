from web.config.settings.base import WebAppBaseSettings
from web.config.settings.environment import Environment


class WebAppProdSettings(WebAppBaseSettings):
    DEBUG: bool = False
    RELOAD: bool = False

    SERVER_HOST: str = '0.0.0.0'
    SERVER_PORT: int = 80
    SERVER_WORKERS: int = 4

    DATABASE_NAME: str = 'prod'

    ENVIRONMENT: Environment = Environment.PRODUCTION
