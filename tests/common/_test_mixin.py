from faker import Generator, Factory

from user.models import User


class TestCaseMixin:
    faker: Generator

    def set_login_and_faker(self):
        self.user: User = User.objects.create_user('test', 'test@test.com', 'test')
        self.client.force_login(self.user)
        faker_ = Factory.create
        self.faker: Generator = faker_()
        self.faker.seed(0)
