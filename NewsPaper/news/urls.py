from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, NewsListWithSearch, NewCreate, ArticleCreate,NewUpdate,ArticleUpdate, NewDelete, ArticleDelete, CommentaryCreate, ArticleList
from .views import subscriptions, IndexView
from django.views.decorators.cache import cache_page

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('news/', NewsList.as_view(),  name = "news_list"),
   path('test', IndexView.as_view()),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('news/<int:pk>/', cache_page(60*10)(NewsDetail.as_view()),  name = "post_detail"),
   path('news/search/', NewsListWithSearch.as_view(), name = "news_search"),
   path('news/create/', NewCreate.as_view(), name='new_create'),
   path('articles/', ArticleList.as_view(), name='article_list'),
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('news/<int:pk>/update/', NewUpdate.as_view(), name='new_update'),
   path('articles/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
   path('news/<int:pk>/delete/', NewDelete.as_view(), name='new_delete'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
   path('news/<int:pk>/addcomment', CommentaryCreate.as_view(),  name = "add_comment"),
   path('subscriptions/', subscriptions, name='subscriptions'),
]