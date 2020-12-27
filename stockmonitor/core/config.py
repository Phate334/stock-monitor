import functools
from pathlib import Path

from pydantic import BaseSettings
from loguru import logger

USER_ENV_NAME = 'stock.env'


class Settings(BaseSettings):
    db_host: str
    db_base: str
    db_user: str = None
    db_pass: str = None

    data_path: Path = Path('data')

    log_path: str = 'log'
    log_rotation: str = '100 MB'
    log_retention: str = '7 days'

    goodinfo_sleep: int = 10

    class Config:
        env_file_encoding = 'utf-8'


@functools.lru_cache()
def get_settings(**kwargs) -> Settings:
    first_env = Path('.env')
    user_env = Path.home().joinpath(USER_ENV_NAME)
    env = first_env if first_env.is_file() else user_env
    logger.info('read config from: ' + str(env))

    return Settings(_env_file=env, **kwargs)
