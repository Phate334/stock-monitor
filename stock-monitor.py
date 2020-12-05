from datetime import datetime
from pathlib import Path

from fire import Fire
from loguru import logger

from stockmonitor.core.config import get_settings
from stockmonitor.fetch.fund import SITCAExpense

settings = get_settings()


class StockMonitor:
    @logger.catch
    def etf(self, year: str = str(datetime.now().year)):
        fund = SITCAExpense(settings.data_path)
        fund_expense = fund.get_table(str(year), update=True, save=True)
        print(len(fund_expense.funds))


if __name__ == '__main__':
    logger.add(Path(settings.log_path).joinpath('stock-monitor.log'),
               rotation=settings.log_rotation,
               retention=settings.log_retention,
               encoding='utf-8',
               compression='zip')
    Fire(StockMonitor)
