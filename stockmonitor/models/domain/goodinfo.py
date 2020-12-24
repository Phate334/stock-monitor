from typing import List

from pydantic import BaseModel

from stockmonitor.models.domain.code import Stock


class GoodInfoBasic(Stock):
    shares: int


class GoodInfoBasicTable(BaseModel):
    stocks: List[GoodInfoBasic] = []
