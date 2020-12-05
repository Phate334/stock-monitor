from typing import List
from pydantic import BaseModel

_SITCA_EXPENSE_ROW = [
    'type_code', 'tax_id', 'name', 'transaction_fee_amount',
    'transaction_fee_ratio', 'transaction_tax_amount', 'transaction_tax_ratio',
    'management_Fee_amount', 'management_Fee_ratio', 'custodian_fee_amount',
    'custodian_fee_ratio', 'guarantee_fee_amount', 'guarantee_fee_ratio',
    'other_fee_amount', 'other_fee_ratio', 'total_amount', 'total_ratio'
]


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

    def add_fund(self, fund: FundExpense) -> None:
        self.funds.append(fund)


class SITCAFormValue(BaseModel):
    year: List[str]
    month: List[str]


def create_from_sitca_expense(row: List[str]) -> FundExpense:
    return FundExpense(**dict(zip(_SITCA_EXPENSE_ROW, row)))
