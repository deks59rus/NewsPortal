from django_filters import FilterSet, DateTimeFilter, DateFromToRangeFilter
from django.forms import DateTimeInput
from .models import Post
from django.db import models as django_models

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class NewsFilter(FilterSet):
    #date_between = DateFromToRangeFilter(field_name="time_of_creation", label="Date (Between)")
    added_after = DateTimeFilter(
        field_name='time_of_creation',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%d',
            attrs={'type': 'datetime-local'},
        ),
    )
    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'post_name': ['icontains'],
           'post_category': ['exact'],
            #"time_of_creation" : ['gt'],
       }
