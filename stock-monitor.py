from datetime import datetime
from pathlib import Path

from fire import Fire
from loguru import logger

from stockmonitor.core.config import get_settings
from stockmonitor import (SITCAExpenseFetcher, FundClearDetailFetcher,
                          FinMindFetcher, MoneyDJFetcher, GoodInfoFetcher)
from stockmonitor.utils.etf import to_etf
from stockmonitor.models.domain.etf import ETFList

settings = get_settings()


class StockMonitor:
    @logger.catch
    def etf(self):
        last_year = str(datetime.now().year - 1)
        sitca_expense_fetcher = SITCAExpenseFetcher()
        fund_expense = sitca_expense_fetcher.get_table(last_year,
                                                       update=True,
                                                       save=True)
        stock_index_fund = [
            f for f in fund_expense.funds if f.type_code.startswith('AH')
        ]
        etf_table = ETFList(year=last_year)

        fund_detail_fetcher = FundClearDetailFetcher()
        for fund in stock_index_fund:
            fund_detail = fund_detail_fetcher.fetch(fund.tax_id)
            if not fund_detail.stock_code:
                continue
            etf_table.funds.append(to_etf(fund_detail, fund))

        fund_detail_fetcher.save()
        etf_path = settings.data_path.joinpath('etf.json')
        with open(etf_path, 'w', encoding='utf-8') as f:
            f.write(etf_table.json(ensure_ascii=False))

    @logger.catch
    def finmind(self):
        f = FinMindFetcher()
        logger.info(
            f.fetch(dataset='TaiwanStockPrice',
                    stock_id='2330',
                    date='2020-12-01',
                    end_date='2020-12-02'))

    @logger.catch
    def etfcontent(self, stock_id: str):
        logger.warning('remember update twstock codes.')
        stock_id = str(stock_id)
        mdj = MoneyDJFetcher()
        gi = GoodInfoFetcher()
        etf_content = mdj.fetch_etf_content(stock_id)
        with open(f'{stock_id}.csv', 'w', encoding='utf-8') as f:
            f.write('code,name,volume,etf_percent,shares,stock_percent\n')
            csv_pattern = '{},{},{},{},{},{}\n'
            for stock in etf_content.stocks:
                try:
                    basic = gi.fetch_basic(stock.code)
                    f.write(
                        csv_pattern.format(
                            stock.code, stock.name, stock.volume,
                            stock.percent, basic.shares,
                            '{:.2%}'.format(stock.volume / basic.shares)))
                except:
                    ...


if __name__ == '__main__':
    logger.add(Path(settings.log_path).joinpath('stock-monitor.log'),
               rotation=settings.log_rotation,
               retention=settings.log_retention,
               encoding='utf-8',
               compression='zip')
    Fire(StockMonitor)
