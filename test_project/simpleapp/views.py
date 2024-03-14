from django.shortcuts import render
from datetime import datetime, timedelta
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from.models import Product, Subscription, Category #Добавляем модели категорий и подписок
from .forms import ProductForm
from pprint import pprint
from django.http import HttpResponse
from .filters import ProductFilter
from django.urls import reverse_lazy
# Импорт задач для ассинхронного выполнения
from django.views import View
from .tasks import hello, printer
# Импорт библиотек от модуля D6
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect# защита доступа
from django.db.models import Exists, OuterRef
from django.shortcuts import render

# Create your views here.
"""
Вот так мы можем использовать дженерик ListView для вывода списка товаров:

Создаем свой класс, который наследуется от ListView.
Указываем модель, из которой будем выводить данные.
Указываем поле сортировки данных модели (необязательно).
Записываем название шаблона.
Объявляем, как хотим назвать переменную в шаблоне.

Пример проверки прав для группы пользователей
from django.contrib.auth.mixins import PermissionRequiredMixin

class MyView(PermissionRequiredMixin, View):
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')
"""
# Пример асинхронного выполнения задачи:
class IndexView(View):
    def get(self, request):
        #printer.delay(N=10) # Пример 1
        printer.apply_async([10], countdown=5) # Пример 2
        # printer.apply_async([10], eta = datetime.now() + timedelta(seconds=5))
        # последний, параметр выполнения — expires. Он служит для того, чтобы убирать задачу из очереди по прошествии какого-то времени.
        hello.delay()
        return HttpResponse('Hello!')
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
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        # Возвращаем из функции отфильтрованный список товаров
        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs
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
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
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

def multiply(request):
   number = request.GET.get('number')
   multiplier = request.GET.get('multiplier')

   try:
       result = int(number) * int(multiplier)
       html = f"<html><body>{number}*{multiplier}={result}</body></html>"
   except (ValueError, TypeError):
       html = f"<html><body>Invalid input.</body></html>"

   return HttpResponse(html)

#Вывод формы подписок на рассылки
@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

class ProductCreate(PermissionRequiredMixin,CreateView):
    permission_required = ('simpleapp.add_product',)
    # Указываем нашу разработанную форму
    form_class = ProductForm
    # модель товаров
    model = Product
    # и новый шаблон, в котором используется форма.
    template_name = 'product_edit.html'
    raise_exception = True

class ProductUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.change_product',)
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'

class ProductDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.delete_product',)
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')