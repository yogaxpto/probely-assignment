from datetime import date, timedelta

import factory
import math
from djmoney.money import Money
from factory import fuzzy
from factory.django import DjangoModelFactory
from faker import Faker

from cash_flow.models import CashFlow, CashFlowType
from loan.models import Loan
from tests.common.factory import LoanFactory
from tests.common.factory import UserFactory
from user.models import User

faker: Faker = Faker()


class CashFlowFactory(DjangoModelFactory):
    user: User = factory.SubFactory(UserFactory)
    loan: Loan = factory.SubFactory(LoanFactory)
    reference_date: date = factory.LazyFunction(
        lambda: faker.date_between_dates(date_start=date.today(), date_end=date.today() + timedelta(days=365 * 5)))
    type = fuzzy.FuzzyChoice([t.value for t in CashFlowType])
    amount = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)

    @factory.post_generation
    def set_amount(self, create, extracted, **kwargs):
        # set the amount based on the type field
        if self.type == CashFlowType.Funding.value:
            self.amount = Money(amount=-abs(self.amount.amount), currency='USD')
        else:
            self.amount = Money(amount=abs(self.amount.amount), currency='USD')

    class Meta:
        model = CashFlow
