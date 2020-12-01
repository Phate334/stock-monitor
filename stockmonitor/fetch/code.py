import abc
from typing import List

import twstock
from requests_html import HTMLSession

from stockmonitor.models.domain.code import Stock, StockPercentage
from stockmonitor.models.source import DataSource


def _twstock_update_helper():
    twstock.__update_codes()


class BaseCodeList(abc.ABC):
    @abc.abstractmethod
    def get_codes(self) -> List:
        return NotImplemented

    @abc.abstractmethod
    def fetch_list(self) -> None:
        return NotImplemented


class TWStockCodeList(BaseCodeList):
    """data from twstock module.
    """
    def get_codes(self) -> List[Stock]:
        for code in twstock.codes.values():
            yield self._to_stock(code)

    def fetch_list(self) -> None:
        _twstock_update_helper()

    def _to_stock(self, code_info) -> Stock:
        return Stock(code=code_info.code,
                     name=code_info.name,
                     start=code_info.start,
                     market=code_info.market,
                     group=code_info.group,
                     isin=code_info.ISIN,
                     cfi=code_info.CFI)


class TAIEXCodeList(BaseCodeList):
    """每月市值排名
    """
    TAIFEX_URL = 'https://www.taifex.com.tw/cht/9/futuresQADetail'
    HISTOCK_URL = 'https://histock.tw/stock/taiexproportion.aspx'
    codes = []

    def __init__(self, source: DataSource = DataSource.TAIFEX) -> None:
        if source == DataSource.HISTOCK:
            raise NotImplementedError
        self.src = source
        self.session = HTMLSession()

    def get_codes(self) -> List[Stock]:
        for code in self.codes:
            yield code

    def fetch_list(self) -> None:
        src_url = self.TAIFEX_URL if self.src == DataSource.TAIFEX else self.HISTOCK_URL
        res = self.session.get(src_url).html
        trs = res.find('tr')[1:]
        for rows in trs:
            row = [td.text for td in rows.find('td')]
            self._add_stock_code(row[:4])
            if row[4:]:
                self._add_stock_code(row[4:])

    def _add_stock_code(self, cols: List[str]) -> StockPercentage:
        self.codes.append(
            StockPercentage(order=cols[0],
                            code=cols[1],
                            name=cols[2],
                            percent=cols[3]))
