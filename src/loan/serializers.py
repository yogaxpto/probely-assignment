from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from loan.models import Loan


class LoanSerializer(ModelSerializer[Loan]):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Loan
        fields = '__all__'
