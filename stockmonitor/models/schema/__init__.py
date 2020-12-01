from peewee import Model, MySQLDatabase

from stockmonitor.core.config import get_settings

settings = get_settings()
database = MySQLDatabase(None)


class BaseModel(Model):
    def __init__(self) -> None:
        database.init(database=settings.db_base,
                      host=settings.db_host,
                      user=settings.db_user,
                      password=settings.db_pass)
