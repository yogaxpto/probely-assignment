import factory
from factory.django import DjangoModelFactory

from user.models import User


class UserFactory(DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:
        model = User
