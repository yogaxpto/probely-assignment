from celery import shared_task
from django.core.cache import cache

from statistic.serializers import StatisticSerializer
from statistic.services import StatisticService


@shared_task
def statistic_task_update_cache(user_id: int) -> None:
    cache.delete(StatisticService.get_user_cache_key(user_id))

    _ = StatisticSerializer({}, context={
        'user_id': user_id}).data
