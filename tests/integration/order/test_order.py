from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from product.models import Product
from tests.common import TestCaseMixin
from tests.common.factory import ProductFactory, OrderFactory


class OrderTests(APITestCase, TestCaseMixin):
    url = '/api/v1/orders/'

    def setUp(self) -> None:
        self.set_login_and_faker()

    def test_create_user_order(self):
        # Arrange
        product: Product = ProductFactory.create()
        data: dict = {
            'quantity': 3,
            'product': product.id
        }

        # Act
        response: Response = self.client.post(self.url, data=data)

        # Assert
        self.assertEqual(status.HTTP_201_CREATED, response.status_code, response.data)
        self.assertEqual(product.id, response.data['product'])
        self.assertEqual(data['quantity'], response.data['quantity'])
        self.assertEqual(self.user.id, response.data['user'])

    def test_create_order_product_decreases_stock(self):
        # Arrange
        product: Product = ProductFactory.create()
        data: dict = {
            'quantity': 3,
            'product': product.id
        }
        expected: int = product.quantity_stock - data['quantity']

        # Act
        response: Response = self.client.post(self.url, data=data)
        actual: int = Product.objects.get(pk=product.id).quantity_stock

        # Assert
        self.assertEqual(status.HTTP_201_CREATED, response.status_code, response.data)
        self.assertEqual(product.id, response.data['product'])
        self.assertEqual(data['quantity'], response.data['quantity'])
        self.assertEqual(expected, actual)

    def test_list_order_filter_user(self):
        # Arrange
        expected = 10
        OrderFactory.create_batch(expected, user=self.user)

        # Act
        response: Response = self.client.get(f'{self.url}?user={self.user.id}')
        actual = len(response.data)

        # Assert
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.assertEqual(expected, actual)
