from typing import List

from pydantic import BaseModel

from stockmonitor.models.domain.code import StockPercentage


class ETFStockContent(BaseModel):
    stocks: List[StockPercentage] = []
    update: str = None

    def __contains__(self, stock_id: str) -> bool:
        return next((True for s in self.stocks if s.code == stock_id), False)
