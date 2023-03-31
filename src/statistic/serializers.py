from django.core.cache import cache
from rest_framework import serializers

from statistic.services import StatisticService


class StatisticSerializer(serializers.Serializer):
    num_loans = serializers.IntegerField()
    total_invested_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    current_invested_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_repaid_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    avg_realized_irr = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)

    def to_representation(self, instance):
        if 'user_id' in self.context:
            user_id = self.context['user_id']
        else:
            user_id = self.context['request'].user.id

        cache_key = StatisticService.get_user_cache_key(user_id)

        data = cache.get(cache_key)
        if data is None:
            data = {
                'num_loans': StatisticService.get_num_loans(user_id),
                'total_invested_amount': StatisticService.get_total_invested_amount(user_id),
                'current_invested_amount': StatisticService.get_current_invested_amount(user_id),
                'total_repaid_amount': StatisticService.get_total_repaid_amount(user_id),
                'avg_realized_irr': StatisticService.get_avg_realized_irr(user_id),
            }
            cache.set(cache_key, data)
        return data
