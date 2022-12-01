from factory.django import DjangoModelFactory
from faker import Factory

from product.models import Product

faker = Factory.create()


class ProductFactory(DjangoModelFactory):
    price: float = 3.6
    quantity_stock: int = 36

    class Meta:
        model = Product
