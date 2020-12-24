from typing import List

from pydantic import BaseModel

from stockmonitor.models.domain.code import StockPercentage


class ETFStockContent(BaseModel):
    stocks: List[StockPercentage] = []
    update: str = None
