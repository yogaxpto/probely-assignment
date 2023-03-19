from rest_framework import serializers


class DataUploadSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    loans = serializers.FileField(required=True, label='Loans CSV File')
    cash_flow = serializers.FileField(required=True, label='Cash Flow CSV File')

    def validate(self, data):
        """
        Check that both files are CSV files.
        """
        loans = data.get('loans')
        cash_flow = data.get('cash_flow')

        file_error_dict: dict = {
            loans: 'loans',
            cash_flow: 'cash_flow'
        }

        for variable, name in file_error_dict.items():
            if not variable.name.endswith('.csv'):
                raise serializers.ValidationError(f'{name} is not a CSV file.')

        return data
