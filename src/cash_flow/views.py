from drf_spectacular.utils import extend_schema_view, extend_schema

from cash_flow.models import CashFlow
from cash_flow.serializers import CashFlowSerializer
from common.view_sets import BaseCreateReadModelViewSet


@extend_schema(tags=['cash_flows'])
@extend_schema_view(
    list=extend_schema(description='List all CashFlows.'),
    retrieve=extend_schema(description='Retrieve a Cash Flow.'),
    create=extend_schema(description='Create a Cash Flow.'),
)
class CashFlowViewSet(BaseCreateReadModelViewSet):
    serializer_class = CashFlowSerializer
    queryset = CashFlow.objects.all()
    filterset_fields = '__all__'
