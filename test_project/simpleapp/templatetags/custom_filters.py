from django import template


register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.

CURRENCIES_SYMBOLS = {
   'rub': 'Р',
   'usd': '$',
}


@register.filter()
def currency(value, code = "rub"):
   """
   value: значение, к которому нужно применить фильтр
   code: код валюты
   """
   # Возвращаемое функцией значение подставится в шаблон.
   postfix = CURRENCIES_SYMBOLS[code]
   return f'{value} {postfix}'