from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from common.view_sets import BaseCreateReadModelViewSet
from order.models import Order
from order.serializers import OrderSerializer


@extend_schema(tags=['orders'])
@extend_schema_view(
    list=extend_schema(description='List all Order.', parameters=[
        OpenApiParameter(name='user', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                         description='Filter all orders related to this user id.')]),
    retrieve=extend_schema(description='Retrieve an Order.'),
    create=extend_schema(description='Create an Order.'),
)
class OrderViewSet(BaseCreateReadModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filterset_fields = ['user']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
