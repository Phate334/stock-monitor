from enum import Enum

class Market(Enum):
    TWSE = 'twse'  # 上市 股票
    TPEX = 'tpex'  # 上櫃 認購(售)權證
