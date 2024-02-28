from django.urls import path
# Импортируем созданное нами представление
from .views import SignUp


urlpatterns = [
   # path — означает путь.
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('signup/', SignUp.as_view(),name = 'signup'),

]