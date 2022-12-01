from django.core.validators import MinValueValidator
from django.db.models import AutoField, FloatField, CharField, IntegerField

from common.models import BaseModel
from user.models import User


class Product(BaseModel):
    id = AutoField(primary_key=True, auto_created=True, editable=False)
    name = CharField(max_length=40)
    price = FloatField(validators=[MinValueValidator(0)])
    quantity_stock = IntegerField(validators=[MinValueValidator(0)])
