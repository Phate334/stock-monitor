from requests_html import HTMLSession

from stockmonitor.models.domain.findmind import Parameters
from stockmonitor.utils.parameter import func_helper


class FinMindFetcher:
    BASE_URL = 'https://api.finmindtrade.com/api/v3/data'

    def __init__(self) -> None:
        self.session = HTMLSession()

    @func_helper(Parameters)
    def taiwan_stock_price(self, parms: Parameters):
        return self._fetch(parms)

    def _fetch(self, parms: Parameters):
        return self.session.get(self.BASE_URL, params=parms).json()
