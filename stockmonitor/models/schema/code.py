from peewee import CharField
from . import BaseModel


class StockCode(BaseModel):
    code = CharField()
    name = CharField()
