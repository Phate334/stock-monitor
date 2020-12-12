from datetime import datetime
from pathlib import Path

from fire import Fire
from loguru import logger

from stockmonitor.core.config import get_settings
from stockmonitor.fetch.fund import SITCAExpenseFetcher, FundClearDetailFetcher
from stockmonitor.fetch.finmind import FinMindFetcher

settings = get_settings()


class StockMonitor:
    @logger.catch
    def etf(self):
        last_year = str(datetime.now().year - 1)
        sitca_expense_fetcher = SITCAExpenseFetcher()
        fund_expense = sitca_expense_fetcher.get_table(last_year,
                                                       update=True,
                                                       save=True)
        etf = [f for f in fund_expense.funds if f.type_code.startswith('AH')]
        fund_detail_fetcher = FundClearDetailFetcher()
        for e in etf:
            fund_detail_fetcher.fetch(e.tax_id)
        fund_detail_fetcher.save()

    @logger.catch
    def finmind(self):
        f = FinMindFetcher()
        logger.info(
            f.taiwan_stock_price(dataset='TaiwanStockPrice',
                                 stock_id='2330',
                                 date='2020-12-01',
                                 end_date='2020-12-02'))


if __name__ == '__main__':
    logger.add(Path(settings.log_path).joinpath('stock-monitor.log'),
               rotation=settings.log_rotation,
               retention=settings.log_retention,
               encoding='utf-8',
               compression='zip')
    Fire(StockMonitor)
