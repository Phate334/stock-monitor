from pydantic import BaseModel


class Parameters(BaseModel):
    dataset: str
    stock_id: str = None
    data_id: str = None
    date: str = None
    end_date: str = None
    user_id: str = None
    password: str = None
