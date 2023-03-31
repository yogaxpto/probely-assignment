from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from common.view_sets import BaseViewSet
from statistic.serializers import StatisticSerializer


@extend_schema(tags=['statistics'])
@extend_schema_view(
    list=extend_schema(description='Retrieve Statistics.'),
)
class StatisticViewSet(BaseViewSet, ListModelMixin):
    serializer_class = StatisticSerializer

    def list(self, request, *args, **kwargs) -> Response:
        return Response(self.get_serializer({}).data, status=status.HTTP_200_OK)
