from datetime import date

import pyxirr
from _decimal import Decimal
from djmoney.money import Money

from cash_flow.models import CashFlow, CashFlowType
from loan.models import Loan


class LoanServices:

    @staticmethod
    def __calculate_xirr(dict_dates_amounts: dict[date, Decimal]) -> float:
        return pyxirr.xirr({key: value.amount for key, value in dict_dates_amounts.items()})

    @staticmethod
    def update_fields_funding(reference_date: date, amount: Money, loan: Loan) -> None:
        loan.investment_date = reference_date
        loan.invested_amount = -amount
        loan.expected_interest_amount = loan.total_expected_interest_amount * (loan.invested_amount / loan.total_amount)
        xirr_data = {
            reference_date: amount,
            loan.maturity_date: loan.invested_amount + loan.expected_interest_amount
        }
        loan.expected_irr = LoanServices.__calculate_xirr(xirr_data)
        loan.save()

    @staticmethod
    def update_fields_repayment(loan: Loan) -> None:
        dict_date_cash_flows: dict[date, Money] = {cf.reference_date: cf.amount for cf in
                                                   CashFlow.objects.filter(loan_id=loan)}
        if sum(dict_date_cash_flows.values()) >= loan.invested_amount + loan.expected_interest_amount:
            loan.is_closed = True
            xirr_data = {
                loan.investment_date: CashFlow.objects.filter(loan=loan,
                                                              type=CashFlowType.Funding.value).first().amount
            } |dict_date_cash_flows
            loan.realized_irr = LoanServices.__calculate_xirr(xirr_data)
            loan.save()
