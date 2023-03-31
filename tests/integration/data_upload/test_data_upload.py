import os
from pathlib import Path

from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from cash_flow.models import CashFlow
from loan.models import Loan
from tests.common import TestCaseMixin


class DataUploadTests(APITestCase, TestCaseMixin):
    url = '/api/v1/data_upload/'

    def setUp(self) -> None:
        self.set_login_and_faker()
        self._file_path = os.path.join(Path(__file__).parent.parent.parent.parent, 'project_files')
        self.loan_csv_path = os.path.join(self._file_path, 'loans.csv')
        self.cash_flow_csv_path = os.path.join(self._file_path, 'cash_flows.csv')

    def test_data_upload_files(self):
        """
        WHEN the endpoint receives valid input
        THEN the data for the loans is stored in the database
            AND the data for the cash flows is stored in the database.
        """
        # Arrange

        with open(self.loan_csv_path, 'r') as loan_file, open(self.cash_flow_csv_path, 'r') as cash_flow_file:
            data = {
                'loans': loan_file,
                'cash_flows': cash_flow_file,
            }

            # Act
            response = self.client.post(self.url, data=data, format='multipart')

            # Assert
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
            self.assertEqual(Loan.objects.count(), 3)
            self.assertEqual(CashFlow.objects.count(), 5)

    def test_data_upload_files_400_error(self):
        """
        WHEN the endpoint receives invalid input
        THEN the database data remains unchanged
            AND the endpoint returns an error of the result.
        """
        # Arrange
        list_test_cases: list[tuple[str, str]] = [
            ('cash_flows_wrong', 'Invalid file type, must be CSV'),
            ('cash_flows_wrong.csv', 'Invalid CSV file format.')
        ]

        for file, error_message in list_test_cases:
            with self.subTest(file=file, error_message=error_message):
                with open(self.loan_csv_path, 'r') as loan_file, open(os.path.join(self._file_path, file),
                                                                      'r') as cash_flow_file:
                    data = {
                        'loans': loan_file,
                        'cash_flows': cash_flow_file,
                    }

                    # Act
                    response = self.client.post(self.url, data=data, format='multipart')

                    # Assert
                    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
                    self.assertEqual([ErrorDetail(string=error_message, code='invalid')], response.data['cash_flows'])
                    self.assertEqual(Loan.objects.count(), 0)
                    self.assertEqual(CashFlow.objects.count(), 0)
