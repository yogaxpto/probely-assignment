from drf_spectacular.utils import extend_schema, extend_schema_view

from common.view_sets import BaseModelViewSet
from user.models import User
from user.serializers import UserSerializer


@extend_schema(tags=['users'])
@extend_schema_view(
    list=extend_schema(description='List all Users.'),
    retrieve=extend_schema(description='Retrieve an User.'),
    update=extend_schema(description='Update an User.'),
    partial_update=extend_schema(description='Patch an User.'),
    destroy=extend_schema(description='Remove an User.'),
)
class UserViewSet(BaseModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
