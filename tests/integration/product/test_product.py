from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from tests.common import TestCaseMixin
from tests.common.factory import ProductFactory


class ProductTests(APITestCase, TestCaseMixin):
    url = '/api/v1/products/'

    def setUp(self) -> None:
        self.set_login_and_faker()

    def test_list_products(self):
        # Arrange
        expected: int = 13
        ProductFactory.create_batch(expected)

        # Act
        response: Response = self.client.get(self.url)
        actual: int = len(response.data)

        # Assert
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.assertEqual(expected, actual)
