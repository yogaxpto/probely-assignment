from enum import IntEnum

from django.db.models import DateField, IntegerField, AutoField, ForeignKey, PROTECT

from common.models import BaseModel, MoneyField
from loan.models import Loan
from user.models import User


class CashFlowType(IntEnum):
    Funding = 1
    Repayment = 2

    @staticmethod
    def choices() -> list[tuple[int, str]]:
        return [(cash_flow.value, cash_flow.name) for cash_flow in CashFlowType]


class CashFlow(BaseModel):
    id = AutoField(primary_key=True)
    user = ForeignKey(User, on_delete=PROTECT)
    loan = ForeignKey(Loan, on_delete=PROTECT)
    reference_date = DateField()
    type = IntegerField(choices=CashFlowType.choices())
    amount = MoneyField()


