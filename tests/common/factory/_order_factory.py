import factory
from factory.django import DjangoModelFactory
from faker import Factory

from order.models import Order
from product.models import Product
from tests.common.factory._product_factory import ProductFactory
from tests.common.factory._user_factory import UserFactory
from user.models import User

faker = Factory.create()


class OrderFactory(DjangoModelFactory):
    user: User = factory.SubFactory(UserFactory)
    product: Product = factory.SubFactory(ProductFactory)
    quantity: int = 33

    class Meta:
        model = Order
