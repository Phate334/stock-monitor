import re
from datetime import date, datetime
from typing import List

from pydantic import BaseModel, ValidationError, validator

_SITCA_EXPENSE_ROW = [
    'type_code', 'tax_id', 'name', 'transaction_fee_amount',
    'transaction_fee_ratio', 'transaction_tax_amount', 'transaction_tax_ratio',
    'management_Fee_amount', 'management_Fee_ratio', 'custodian_fee_amount',
    'custodian_fee_ratio', 'guarantee_fee_amount', 'guarantee_fee_ratio',
    'other_fee_amount', 'other_fee_ratio', 'total_amount', 'total_ratio'
]

FUND_CLEAR_TITLE_MAP = {
    '基金統編': 'tax_id',
    '基金中文名稱': 'name',
    '投信事業': 'company',
    '基金ISINCODE': 'isincode',
    '受益憑證代號': 'stock_code',
    '基金計價幣別': 'currency',
    '基金成立日': 'start',
    '基金規模(新台幣)': 'scale',
    '規模日期': 'scale_update',
    '基金種類': 'fund_class',
    '投資標的': 'fund_target',
    '資料更新日期': 'modify_date',
}

TW_DATE_PATTERN = re.compile(r'(\d{4})\D(\d{2})\D(\d{2})\D')
DATE_PATTERN = re.compile(r'\d{4}-\d{2}-\d{2}')


class FundExpense(BaseModel):
    type_code: str
    tax_id: str
    name: str
    transaction_fee_amount: str
    transaction_fee_ratio: str
    transaction_tax_amount: str
    transaction_tax_ratio: str
    management_Fee_amount: str
    management_Fee_ratio: str
    custodian_fee_amount: str
    custodian_fee_ratio: str
    guarantee_fee_amount: str
    guarantee_fee_ratio: str
    other_fee_amount: str
    other_fee_ratio: str
    total_amount: str
    total_ratio: str


class SITCAExpenseTable(BaseModel):
    funds: List[FundExpense] = []


class SITCAFormValue(BaseModel):
    year: List[str]
    month: List[str]


class FundClearDetail(BaseModel):
    tax_id: str
    name: str = None
    company: str = None
    isincode: str = None
    stock_code: str = None
    currency: str = None
    start: str = None
    scale: str = None
    scale_update: str = None
    fund_class: str = None
    fund_target: str = None
    modify_date: str = None

    @validator('start', 'scale_update', pre=True)
    def cleanup_date(cls, date: str):
        if not date:
            return None
        res = TW_DATE_PATTERN.match(date)
        if res:
            return '{}-{}-{}'.format(res.group(1), res.group(2), res.group(3))
        elif DATE_PATTERN.match(date):
            return date
        raise ValidationError('start or scale_update not in pattern: ' + date)


class FundClearDetailList(BaseModel):
    funds: List[FundClearDetail] = []


def create_from_sitca_expense(row: List[str]) -> FundExpense:
    return FundExpense(**dict(zip(_SITCA_EXPENSE_ROW, row)))
