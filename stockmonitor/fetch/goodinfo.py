from pathlib import Path
from time import sleep

from twstock import codes
from requests_html import HTMLSession
from loguru import logger

from stockmonitor.models.domain.goodinfo import GoodInfoBasic, GoodInfoBasicTable


class GoodInfoFetcher:
    BASIC_URL = 'https://goodinfo.tw/StockInfo/BasicInfo.asp?STOCK_ID={}'

    def __init__(self, data_dir: Path = Path('data')) -> None:
        self.session = HTMLSession()
        self.goodinfo_data = data_dir.joinpath('goodinfo')
        self.goodinfo_data.mkdir(parents=True, exist_ok=True)
        self.basic_path = self.goodinfo_data.joinpath('basic.json')
        self.basic = None

    def fetch_basic(self, stock_id: str) -> GoodInfoBasic:
        if not self.basic:
            if self.basic_path.is_file():
                self.basic = GoodInfoBasicTable.parse_file(self.basic_path)
            else:
                self.basic = GoodInfoBasicTable()
        result = next((s for s in self.basic.stocks if s.code == stock_id),
                      None)
        if not result:
            result = self._download_basic(stock_id)
            self.basic.stocks.append(result)
            self._save_basic()

        return result

    def _download_basic(self, stock_id: str) -> GoodInfoBasic:
        logger.info(f'download basic {stock_id} from goodinfo')
        html = self.session.get(self.BASIC_URL.format(stock_id)).html
        shares = [
            tr.find('nobr')[1].text
            for tr in html.find('tr,td[bgcolor="white"]')
            if '發行股數' in tr.find('td', first=True).text
        ][0].split('\xa0')[0].replace(',', '')
        sleep(10)

        return GoodInfoBasic(code=stock_id,
                             name=codes[stock_id].name,
                             shares=shares)

    def _save_basic(self):
        with open(self.basic_path, 'w', encoding='utf-8') as f:
            f.write(self.basic.json(ensure_ascii=False, exclude_none=True))
