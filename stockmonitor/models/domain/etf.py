from typing import List
from pydantic import BaseModel


class ETF(BaseModel):
    stock_code: str
    name: str
    company: str
    start: str
    total_ratio: str
    type_code: str


class ETFList(BaseModel):
    funds: List[ETF] = []
    year: str
