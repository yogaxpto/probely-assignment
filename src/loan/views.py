from drf_spectacular.utils import extend_schema, extend_schema_view

from common.view_sets import BaseReadModelViewSet
from loan.models import Loan
from loan.serializers import LoanSerializer


@extend_schema(tags=['loans'])
@extend_schema_view(
    list=extend_schema(description='List all CashFlows.'),
    retrieve=extend_schema(description='Retrieve a Cash Flow.'))
class LoanViewSet(BaseReadModelViewSet):
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    filterset_fields = '__all__'
