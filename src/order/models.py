from django.core.validators import MinValueValidator
from django.db.models import ForeignKey, PROTECT, AutoField, IntegerField

from common.models import BaseModel
from product.models import Product
from user.models import User


class Order(BaseModel):
    id = AutoField(primary_key=True, auto_created=True, editable=False)
    user = ForeignKey(User, on_delete=PROTECT)
    product = ForeignKey(Product, on_delete=PROTECT)
    quantity = IntegerField(validators=[MinValueValidator(0)])
