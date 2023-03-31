from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet


class BaseViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]


class BaseModelViewSet(ModelViewSet, BaseViewSet):
    pass


class BaseReadModelViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           BaseViewSet):
    pass


class BaseCreateReadModelViewSet(mixins.CreateModelMixin,
                                 BaseReadModelViewSet):
    pass
