from django.db.models import Sum, Avg, Case, When, F, FloatField

from cash_flow.models import CashFlow
from loan.models import Loan


class StatisticService:

    @staticmethod
    def get_user_cache_key(user_id: int):
        return f'statistics:{user_id}'

    @staticmethod
    def get_num_loans(user_id):
        return Loan.objects.filter(user=user_id).count()

    @staticmethod
    def get_total_invested_amount(user_id):
        return Loan.objects.filter(user=user_id).aggregate(Sum('invested_amount'))['invested_amount__sum'] or 0

    @staticmethod
    def get_current_invested_amount(user_id):
        return Loan.objects.filter(user=user_id, is_closed=False).aggregate(Sum('invested_amount'))[
            'invested_amount__sum'] or 0

    @staticmethod
    def get_total_repaid_amount(user_id):
        return CashFlow.objects.filter(user=user_id, loan__is_closed=True).aggregate(Sum('amount'))['amount__sum'] or 0

    @staticmethod
    def get_avg_realized_irr(user_id):
        return Loan.objects.filter(user=user_id, is_closed=True).aggregate(
            weighted_avg_realized_irr=Avg(
                Case(
                    When(realized_irr__gt=0, then=F('realized_irr') * F('invested_amount')),
                    output_field=FloatField(),
                ),
            )
        )['weighted_avg_realized_irr'] or 0
