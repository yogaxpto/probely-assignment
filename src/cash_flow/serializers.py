from functools import partial
from typing import Callable

from celery.result import AsyncResult
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from cash_flow.exceptions import CashFlowWithoutPreviousFundingException, CashFlowFundingAlreadyCreated
from cash_flow.models import CashFlow, CashFlowType
from loan.services import LoanServices
from statistic.tasks import statistic_task_update_cache


class CashFlowSerializer(ModelSerializer[CashFlow]):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = CashFlow
        fields = '__all__'

    @staticmethod
    def _validate(validated_data):
        cf_type: CashFlowType = validated_data.get('type')
        loan = validated_data.get('loan')

        if cf_type == CashFlowType.Repayment and not CashFlow.objects.filter(loan=loan,
                                                                             type=CashFlowType.Funding).exists():
            raise CashFlowWithoutPreviousFundingException

        if cf_type == CashFlowType.Funding and CashFlow.objects.filter(loan=loan,
                                                                       type=CashFlowType.Funding).exists():
            raise CashFlowFundingAlreadyCreated

    def to_internal_value(self, data):
        if 'type' in data:
            data['type'] = CashFlowType[data.pop('type')].value
        return super().to_internal_value(data)

    def to_representation(self, instance: CashFlow):
        return super().to_representation(instance) | {
            'type': CashFlowType(instance.type).name}

    def create(self, validated_data):
        self._validate(validated_data)
        instance: CashFlow = super().create(validated_data)
        instance.refresh_from_db()
        dict_calculations: dict[str, Callable] = {
            'Funding': partial(LoanServices.update_fields_funding, instance.reference_date, instance.amount),
            'Repayment': partial(LoanServices.update_fields_repayment)
        }
        dict_calculations[CashFlowType(instance.type).name](instance.loan)
        statistic_task_update_cache.delay(validated_data.get('user').id)
        return instance
