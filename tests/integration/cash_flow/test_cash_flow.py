from datetime import datetime

from _decimal import Decimal
from djmoney.money import Money
from rest_framework import status
from rest_framework.test import APITestCase

from cash_flow.models import CashFlowType
from loan.models import Loan
from tests.common import TestCaseMixin
from tests.common.factory import CashFlowFactory
from tests.common.factory import LoanFactory


class CashFlowTests(APITestCase, TestCaseMixin):
    url = '/api/v1/cash_flows/'

    def setUp(self) -> None:
        amount: Money = Money(33, 'USD')
        self.set_login_and_faker()
        self.loan: Loan = LoanFactory.create(total_amount=amount,
                                             total_expected_interest_amount=55,
                                             expected_interest_amount=0,
                                             invested_amount=None,
                                             investment_date=None,
                                             user=self.user)
        self.data: dict = {
            'user': self.user.id,
            'loan': self.loan.id,
            'reference_date': datetime.now().date(),
            'type': 'Funding',
            'amount': -amount.amount
        }

    def test_cash_flow_first_flow_funding(self):
        """
        GIVEN a loan without Cash Flows of type 'Funding'
        WHEN the endpoint receives valid input of type 'Funding'
        THEN the data is stored in the database
            AND the corresponding loan is updated on the field 'investment_date'
            AND the corresponding loan is updated on the field 'invested_amount'
            AND the corresponding loan is updated on the field 'expected_interest_amount'
            AND the corresponding Loan is updated on the field 'expected_irr'
            AND the endpoint returns a success result with the data stored.
        """
        # Arrange
        # Act
        response = self.client.post(self.url, data=self.data)
        self.loan.refresh_from_db()

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(self.data['reference_date'], self.loan.investment_date)
        self.assertEqual(-self.data['amount'], self.loan.invested_amount.amount)
        self.assertEqual(Money(55, 'USD'), self.loan.expected_interest_amount)
        self.assertEqual(0.5609224519797794, self.loan.expected_irr)

    def test_cash_flow_first_flow_repayment(self):
        """
        GIVEN a loan without Cash Flows of type 'Funding'
        WHEN the endpoint receives valid input of type 'Repayment'
        THEN database remains unchanged
            AND the endpoint returns a fail result with an error of the result.
        """
        # Arrange
        payload = self.data | {
            'type': 'Repayment'}

        # Act
        response = self.client.post(self.url, data=payload)
        self.loan.refresh_from_db()

        # Assert
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED, response.data)
        self.assertEqual('Cannot create Repayment Cash Flow for loan without Funding Cash Flow.',
                         str(response.data['detail']))
        self.assertEqual(None, self.loan.investment_date)
        self.assertEqual(None, self.loan.invested_amount)
        self.assertEqual(Money(0, 'USD'), self.loan.expected_interest_amount)
        self.assertEqual(0, self.loan.expected_irr)

    def test_cash_flow_flow_funding(self):
        """
        GIVEN a loan with one Cash Flow of type 'Funding'
        WHEN the endpoint receives valid input of type 'Funding'
        THEN database remains unchanged
            AND the endpoint returns a fail result with an error of the result.
        """
        # Arrange
        CashFlowFactory.create(type=CashFlowType.Funding, loan=self.loan, user=self.user)

        # Act
        response = self.client.post(self.url, data=self.data)
        self.loan.refresh_from_db()
        # Assert
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED, response.data)
        self.assertEqual('Cannot create Funding Cash Flow for loan with Funding.', str(response.data['detail']))
        self.assertEqual(None, self.loan.investment_date)
        self.assertEqual(None, self.loan.invested_amount)
        self.assertEqual(Money(0, 'USD'), self.loan.expected_interest_amount)
        self.assertEqual(0, self.loan.expected_irr)

    def test_cash_flow_flow_repayment_no_close(self):
        """
        GIVEN a loan with one Cash Flow of type 'Funding'
        WHEN the endpoint receives valid input
            AND the input is of type 'Repayment'
            AND the input amount is lower than the corresponding Loan's 'total_amount'
        THEN Cash Flow is stored
            AND the corresponding Loan's 'is_closed' is FALSE
            AND the endpoint returns success a result with the data stored.
        """
        # Arrange
        amount = -self.data['amount']
        self.loan: Loan = LoanFactory.create(total_amount=amount,
                                             total_expected_interest_amount=amount * Decimal(0.2),
                                             invested_amount=-amount,
                                             user=self.user)
        CashFlowFactory.create(type=CashFlowType.Funding, loan=self.loan, user=self.user)
        payload = self.data | {
            'type': 'Repayment',
            'amount': amount / 2,
            'loan': self.loan.id,
        }

        # Act
        response = self.client.post(self.url, data=payload)
        self.loan.refresh_from_db()

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(False, self.loan.is_closed)

    def test_cash_flow_flow_repayment_close(self):
        """
        GIVEN a loan with one Cash Flow of type 'Funding'
        WHEN the endpoint receives valid input
            AND the input is of type 'Repayment'
            AND the input amount is higher than the corresponding Loan's 'total_amount'
        THEN Cash Flow is stored
            AND the corresponding Loan's 'is_closed' is TRUE
            AND the corresponding loan is updated on the field 'realized_irr'
            AND the endpoint returns success a result with the data stored.
        """
        # Arrange
        amount: Money = Money(-self.data['amount'], 'USD')
        self.loan: Loan = LoanFactory.create(total_amount=amount,
                                             expected_interest_amount=amount * 0.2,
                                             total_expected_interest_amount=amount * 1.2,
                                             invested_amount=-amount,
                                             user=self.user)
        CashFlowFactory.create(type=CashFlowType.Funding, loan=self.loan, user=self.user,
                                   amount=-amount)
        payload = self.data | {
            'type': 'Repayment',
            'amount': (amount * 2).amount,
            'loan': self.loan.id,
        }

        # Act
        response = self.client.post(self.url, data=payload)
        self.loan.refresh_from_db()

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(True, self.loan.is_closed)
