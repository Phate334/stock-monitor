from stockmonitor.models.domain.etf import ETF
from stockmonitor.models.domain.fund import FundClearDetail, FundExpense


def to_etf(fund_detail: FundClearDetail, expense: FundExpense) -> ETF:
    return ETF(stock_code=fund_detail.stock_code,
               name=fund_detail.name,
               company=fund_detail.company,
               start=fund_detail.start,
               total_ratio=expense.total_ratio,
               type_code=expense.type_code)
