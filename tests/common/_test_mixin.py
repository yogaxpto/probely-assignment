from faker import Generator, Factory

from tests.common.factory import UserFactory
from user.models import User


class TestCaseMixin:
    faker: Generator

    def set_login_and_faker(self):
        self.user: User = UserFactory()
        self.client.force_login(self.user)
        faker_ = Factory.create
        self.faker: Generator = faker_()
        self.faker.seed(0)
