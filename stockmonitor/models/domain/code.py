from datetime import datetime

from pydantic import BaseModel, validator

from stockmonitor.models.market import Market


class Stock(BaseModel):
    code: str
    name: str
    isin: str = None
    start: datetime = None
    market: Market = None
    group: str = None
    cfi: str = None

    @validator('start', pre=True)
    def start_date(cls, date_: str) -> datetime:
        return datetime.strptime(date_, '%Y/%m/%d')

    @validator('market', pre=True)
    def market_enum(cls, in_: str) -> Market:
        if in_ == '上市':
            return Market.TWSE
        elif in_ == '上櫃':
            return Market.TPEX
        return None


class StockPercentage(Stock):
    order: int
    percent: float

    @validator('order', pre=True)
    def order_number(cls, in_) -> int:
        return int(in_)

    @validator('percent', pre=True)
    def percent_number(cls, in_) -> float:
        if isinstance(in_, str) and in_[-1] == '%':
            return float(in_[:-1])
        return in_