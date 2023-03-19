from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from data_upload.serializers import DataUploadSerializer


class DataUploadView(APIView):
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
        serializer = DataUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Get the validated data
            loans = serializer.validated_data['loans']
            cash_flow = serializer.validated_data['cash_flow']

            # Your file upload code here
            # ...

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

