from rest_framework.fields import CurrentUserDefault
from rest_framework.serializers import ModelSerializer

from order.errors import InvalidQuantityValidationError
from order.models import Order
from product.models import Product


def _transfer_amount(product: Product, quantity: int) -> None:
    product.quantity_stock -= quantity
    product.save()


def _has_valid_amount(product: Product, quantity: int) -> bool:
    return product.quantity_stock - quantity >= 0


class OrderSerializer(ModelSerializer[Order]):
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'read_only': True,
                'default': CurrentUserDefault()
            }
        }

    def validate(self, attrs: dict) -> dict:
        if not _has_valid_amount(**attrs):
            raise InvalidQuantityValidationError
        return attrs

    def save(self, **kwargs):
        _transfer_amount(**self.validated_data)
        return super().save(**kwargs)
