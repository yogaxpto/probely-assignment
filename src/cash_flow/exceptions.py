from rest_framework import status
from rest_framework.exceptions import APIException


class CashFlowWithoutPreviousFundingException(APIException):
    status_code = status.HTTP_412_PRECONDITION_FAILED
    default_detail = 'Cannot create Repayment Cash Flow for loan without Funding Cash Flow.'


class CashFlowFundingAlreadyCreated(APIException):
    status_code = status.HTTP_412_PRECONDITION_FAILED
    default_detail = 'Cannot create Funding Cash Flow for loan with Funding.'
