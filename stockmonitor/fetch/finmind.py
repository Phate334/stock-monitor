from requests_html import HTMLSession

from stockmonitor.models.domain.findmind import Parameters
from stockmonitor.utils.parameter import func_helper


class FinMindFetcher:
    BASE_URL = 'https://api.finmindtrade.com/api/v3/data'

    def __init__(self) -> None:
        self.session = HTMLSession()

    @func_helper(Parameters)
    def fetch(self, params):
        return self.session.get(self.BASE_URL, params=params).json()
