from datetime import date, timedelta

import factory
from djmoney.money import Money
from factory.django import DjangoModelFactory
from faker import Faker

from loan.models import Loan
from tests.common.factory import UserFactory
from user.models import User

faker: Faker = Faker()

_amount = Money(55, 'USD')


class LoanFactory(DjangoModelFactory):
    id = factory.Sequence(lambda n: faker.uuid4()[:40])
    user: User = factory.SubFactory(UserFactory)
    issue_date = factory.LazyFunction(lambda: faker.date_object())
    investment_date = date.today()
    rating = factory.LazyFunction(lambda: faker.random_int(min=1, max=10))
    maturity_date = factory.LazyFunction(
        lambda: faker.date_between_dates(date_start=date.today(), date_end=date.today() + timedelta(days=365 * 5)))
    invested_amount = _amount
    expected_interest_amount = _amount * 0.2
    total_expected_interest_amount = _amount * 1.2

    class Meta:
        model = Loan
