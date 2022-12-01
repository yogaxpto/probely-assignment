from drf_spectacular.utils import extend_schema, extend_schema_view

from common.view_sets import BaseModelViewSet
from product.models import Product
from product.serializers import ProductSerializer


@extend_schema(tags=['products'])
@extend_schema_view(
    list=extend_schema(description='List all Products.'),
    retrieve=extend_schema(description='Retrieve an Product.'),
    create=extend_schema(description='Create an Product.'),
    update=extend_schema(description='Update an Product.'),
    partial_update=extend_schema(description='Patch an Product.'),
    destroy=extend_schema(description='Remove an Product.'),
)
class ProductViewSet(BaseModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
