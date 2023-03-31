from django.db.models import CharField, DateField, BooleanField, FloatField, IntegerField, ForeignKey, PROTECT

from common.models import BaseModel
from common.models import BaseModel, MoneyField
from user.models import User


class Loan(BaseModel):
    id = CharField(primary_key=True, max_length=40)
    user = ForeignKey(User, on_delete=PROTECT)
    issue_date = DateField()
    total_amount = MoneyField()
    rating = IntegerField(choices=[(x, x) for x in range(1, 10)])
    maturity_date = DateField()
    total_expected_interest_amount = MoneyField()
    invested_amount = MoneyField(null=True)
    investment_date = DateField(null=True)
    expected_interest_amount = MoneyField(default=0)
    is_closed = BooleanField(default=False)
    expected_irr = FloatField(default=0)
    realized_irr = FloatField(default=0)
