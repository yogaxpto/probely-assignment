from django.db.models import DecimalField


class MoneyField(DecimalField):
    def __init__(self, *args, **kwargs) -> None:
        kwargs['max_digits'] = 19
        kwargs['decimal_places'] = 4
        super().__init__(*args, **kwargs)
