from django.shortcuts import render
from datetime import datetime
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView
from.models import Product
from pprint import pprint

# Create your views here.
"""
Вот так мы можем использовать дженерик ListView для вывода списка товаров:

Создаем свой класс, который наследуется от ListView.
Указываем модель, из которой будем выводить данные.
Указываем поле сортировки данных модели (необязательно).
Записываем название шаблона.
Объявляем, как хотим назвать переменную в шаблоне.
"""
class ProductsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Product
    # Поле для порядка сортировки
    ordering = "name"
    # Имя файла шаблона(как представить объекты)
    template_name = "products.html"
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        pprint(context)
        return context

class ProductDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Product
    # Используем другой шаблон — new.html
    template_name = 'product.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'product'
    pk_url_kwarg = "id"