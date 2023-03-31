from datetime import datetime
from unittest.mock import patch, MagicMock

from django.core.cache import cache
from djmoney.money import Money
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from cash_flow.models import CashFlowType
from loan.models import Loan
from statistic.services import StatisticService
from tests.common import TestCaseMixin
from tests.common.factory import CashFlowFactory
from tests.common.factory import LoanFactory
from tests.integration.cash_flow.test_cash_flow import CashFlowTests


class StatisticTests(APITestCase, TestCaseMixin):
    url = '/api/v1/statistics/'
    url_cash_flow = CashFlowTests.url

    def setUp(self) -> None:
        self.set_login_and_faker()
        self.cache_key = StatisticService.get_user_cache_key(self.user.id)
        self.loan: Loan = LoanFactory.create(total_amount=Money(33, 'USD'),
                                             total_expected_interest_amount=55,
                                             expected_interest_amount=0,
                                             invested_amount=None,
                                             investment_date=None,
                                             user=self.user)
        self.cash_flow_payload: dict = {
            'user': self.user.id,
            'loan': self.loan.id,
            'reference_date': datetime.now().date(),
            'type': 'Funding',
            'amount': -self.loan.total_amount.amount
        }

    def tearDown(self) -> None:
        cache.delete(self.cache_key)

    def test_list_statistics_create_data(self):
        """
        GIVEN a Loan with no CashFlow
            AND the cache has unrelated data.
        WHEN the statistics endpoint receives a GET request
        THEN the database provides the data
            AND the endpoint returns the data
            AND the cache saves a copy of the data
        """
        # Arrange
        expected: dict = {
            'num_loans': 1,
            'total_invested_amount': 0,
            'current_invested_amount': 0,
            'total_repaid_amount': 0,
            'avg_realized_irr': 0}

        # Act
        pre_response_cache = cache.get(self.cache_key)
        response: Response = self.client.get(self.url)
        post_response_cache = cache.get(self.cache_key)

        # Assert
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(expected, response.data)
        self.assertEqual(None, pre_response_cache)
        self.assertDictEqual(expected, post_response_cache)

    def test_list_statistics_cache_data(self):
        """
        GIVEN a Loan with CashFlow
            AND the cache has related data.
        WHEN the statistics endpoint receives a GET request
        THEN the cache provides the data
            AND the endpoint returns the data
        """
        # Arrange
        CashFlowFactory.create(type=CashFlowType.Funding, loan=self.loan, user=self.user)
        expected: dict = {
            'num_loans': 1,
            'total_invested_amount': -1,
            'current_invested_amount': -2,
            'total_repaid_amount': -3,
            'avg_realized_irr': -4}
        cache.set(self.cache_key, expected)

        # Act
        response: Response = self.client.get(self.url)

        # Assert
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual(expected, response.data)

    @patch('statistic.tasks.statistic_task_update_cache.delay')
    def test_list_statistics_update_data(self, mock_task: MagicMock):
        """
        GIVEN a Loan with CashFlow
            AND the cache has related data.
        WHEN the CashFlow endpoint receives valid data
            AND the statistics endpoint receives a GET request
        THEN the cache updates the data
            AND the cache provides the new data to the statistics endpoint
            AND the statistics endpoint returns the data
        """
        # Arrange
        cache_data: dict = {
            'num_loans': 1,
            'total_invested_amount': -1,
            'current_invested_amount': -2,
            'total_repaid_amount': -3,
            'avg_realized_irr': -4}
        cache.set(self.cache_key, cache_data)

        def mock_function(_):
            cache.set(self.cache_key, cache_data | {
                'total_repaid_amount': 0,
                'avg_realized_irr': 0
            })

        mock_task.side_effect = mock_function
        # Act
        cash_flow_response = self.client.post(self.url_cash_flow, data=self.cash_flow_payload)
        response: Response = self.client.get(self.url)

        # Assert
        self.assertEqual(status.HTTP_201_CREATED, cash_flow_response.status_code, cash_flow_response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        mock_task.assert_called_once_with(self.user.id)
        self.assertEqual(0, response.data['total_repaid_amount'])
        self.assertEqual(0, response.data['avg_realized_irr'])

    @patch('statistic.tasks.statistic_task_update_cache.delay')
    def test_list_statistics_invalid_cashflow_data(self, mock_task: MagicMock):
        """
        GIVEN a Loan with CashFlow
            AND the cache has related data.
        WHEN the CashFlow endpoint receives invalid data
            AND the statistics endpoint receives a GET request
        THEN the cache remains unchanged
            AND the cache provides the data to the statistics endpoint
            AND the statistics endpoint returns the data
        """
        # Arrange
        CashFlowFactory.create(type=CashFlowType.Funding, loan=self.loan, user=self.user)
        expected: dict = {
            'num_loans': 1,
            'total_invested_amount': -1,
            'current_invested_amount': -2,
            'total_repaid_amount': -3,
            'avg_realized_irr': -4}
        cache.set(self.cache_key, expected)

        def mock_function(_):
            cache.set(self.cache_key, expected | {
                'total_repaid_amount': 0,
                'avg_realized_irr': 0
            })

        mock_task.side_effect = mock_function
        # Act
        cash_flow_response = self.client.post(self.url_cash_flow, data=self.cash_flow_payload)
        response: Response = self.client.get(self.url)

        # Assert
        self.assertEqual(status.HTTP_412_PRECONDITION_FAILED, cash_flow_response.status_code, cash_flow_response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.assertDictEqual(expected, response.data)
        mock_task.assert_not_called()
