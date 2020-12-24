import re
from typing import List

from twstock import codes
from requests_html import HTMLSession

from stockmonitor.models.domain.code import StockPercentage
from stockmonitor.models.domain.moneydj import ETFStockContent

NUM_PATTERN = re.compile(r'[,.]')


class MoneyDJFetcher:
    ETF_CONTENT_URL = 'https://www.moneydj.com/ETF/X/Basic/Basic0007A.xdjhtm?etfid={}.TW'

    def __init__(self):
        self.session = HTMLSession()

    def fetch_etf_content(self, stock_id: str) -> ETFStockContent:
        html = self.session.get(self.ETF_CONTENT_URL.format(stock_id)).html
        date = html.find('#ctl00_ctl00_MainContent_MainContent_sdate3',
                         first=True).text.split('：')[1]
        return ETFStockContent(stocks=self._parse_content(html), update=date)

    def _parse_content(self, html) -> List[StockPercentage]:
        rows = self._table_rows(html, 'table#Repeater1') + self._table_rows(
            html, 'table#Repeater2')
        result = []
        for row in rows:
            name = row.find('.col05', first=True).text
            code = next(
                (codes[c].code for c in codes if codes[c].name == name))
            volume = int(
                re.sub(NUM_PATTERN, '',
                       row.find('.col06', first=True).text)) * 10
            per = row.find('.col07', first=True).text
            result.append(
                StockPercentage(code=code,
                                name=name,
                                volume=volume,
                                percent=per))
        return result

    def _table_rows(self, html, table) -> List:
        return html.find(table, first=True).find('tr')[1:]
