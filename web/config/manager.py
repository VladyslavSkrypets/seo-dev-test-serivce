import os
from functools import lru_cache

from web.config.settings.base import WebAppBaseSettings
from web.config.settings.development import WebAppDevSettings
from web.config.settings.environment import Environment
from web.config.settings.production import WebAppProdSettings


class WebAppSettingsFactory:
    def __init__(self, environment: str):
        self.environment = environment

    def __call__(self) -> WebAppBaseSettings:
        if self.environment == Environment.DEVELOPMENT.value:
            return WebAppDevSettings()
        return WebAppProdSettings()


@lru_cache()
def get_settings() -> WebAppBaseSettings:
    env = os.getenv('ENVIRONMENT', 'DEV')
    return WebAppSettingsFactory(environment=env)()


settings: WebAppBaseSettings = get_settings()
