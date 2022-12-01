from rest_framework.serializers import ModelSerializer

from user.models import User


class UserSerializer(ModelSerializer[User]):
    class Meta:
        model = User
        read_only_fields = ('date_joined', 'is_active', 'last_login')
        exclude = ('groups', 'user_permissions', 'is_staff')

    def create(self, validated_data):
        result: User = super().create(validated_data)
        result.set_password(validated_data['password'])
        result.save()
        return result
