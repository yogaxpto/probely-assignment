from djmoney.models.fields import MoneyField as Mf


class MoneyField(Mf):
    def __init__(self, *args, **kwargs) -> None:
        kwargs['max_digits'] = 19
        kwargs['decimal_places'] = 4
        kwargs['default_currency'] = 'USD'
        super().__init__(*args, **kwargs)
