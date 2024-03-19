from django.urls import path
# Импортируем созданное нами представление
from .views import ProductsList, ProductDetail, multiply, ProductCreate, ProductUpdate, ProductDelete\
   , subscriptions, IndexView
from django.views.decorators.cache import cache_page


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', cache_page(60*10)(ProductsList.as_view()),name = 'product_list'),
   path('test', IndexView.as_view()),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:id>', cache_page(60*10)(ProductDetail.as_view()), name = 'product_detail'),
   path('multiply/', multiply),
   path('create/', ProductCreate.as_view(), name='product_create'),
   path('<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
   path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),
]