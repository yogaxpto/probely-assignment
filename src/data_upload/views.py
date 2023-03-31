from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from common.view_sets import BaseViewSet
from data_upload.serializers import DataUploadSerializer


@extend_schema(tags=['data_upload'])
class DataUploadView(BaseViewSet):
    parser_classes = [MultiPartParser]

    @extend_schema(
        request=DataUploadSerializer,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_400_BAD_REQUEST: 'Invalid CSV file(s)',
        },
        description='Uploads two CSV files.',
        summary='Upload CSV files'
    )
    def post(self, request):
        serializer = DataUploadSerializer(data=request.data, context=super().get_serializer_context())
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
