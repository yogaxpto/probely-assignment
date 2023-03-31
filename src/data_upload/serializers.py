import csv
from io import TextIOWrapper

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed, ValidationError

from cash_flow.serializers import CashFlowSerializer
from loan.serializers import LoanSerializer


def _validate_csv_file(value: InMemoryUploadedFile, data: TextIOWrapper):
    if not value.name.endswith('.csv'):
        raise ValidationError('Invalid file type, must be CSV')
    rows: list[dict] = list(csv.DictReader(data))
    for row in rows:
        if any([value in ['', None] for value in row.values()]):
            raise ValidationError('Invalid CSV file format.')


class LoanBulkSerializer(LoanSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    identifier = serializers.CharField(source='id')
    id = serializers.CharField(read_only=True)

    def create(self, validated_data):
        return super().create(validated_data)


class CashFlowBulkSerializer(CashFlowSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def to_internal_value(self, data):
        if 'loan_identifier' in data:
            data['loan'] = data.pop('loan_identifier')

        return super().to_internal_value(data)


class DataUploadSerializer(serializers.Serializer):
    loans = serializers.FileField()
    cash_flows = serializers.FileField()

    def to_internal_value(self, data):
        data['loans_data'] = TextIOWrapper(data['loans'], encoding='utf-8')
        data['cash_flows_data'] = TextIOWrapper(data['cash_flows'], encoding='utf-8')
        return super().to_internal_value(data)

    def validate_loans(self, value):
        _validate_csv_file(value, self.initial_data['loans_data'])
        return value

    def validate_cash_flows(self, value):
        _validate_csv_file(value, self.initial_data['cash_flows_data'])
        return value

    def create(self, validated_data):
        loans = self.initial_data['loans_data']
        cash_flows = self.initial_data['cash_flows_data']

        return {
            'loans': self._serialize_csv_data(loans, LoanBulkSerializer),
            'cash_flows': self._serialize_csv_data(cash_flows, CashFlowBulkSerializer)}

    def update(self, instance, validated_data):
        raise MethodNotAllowed('Update', detail='This serializer is only meant for creating instances.')

    def _serialize_csv_data(self, file: InMemoryUploadedFile, serializer: type[serializers.ModelSerializer]):
        file.seek(0)
        data: list[dict] = [row for row in csv.DictReader(file.read().splitlines())]  # noqa
        serializer_instance = serializer(data=data, many=True, context=self.context)
        serializer_instance.is_valid(raise_exception=True)
        return serializer_instance.save()
