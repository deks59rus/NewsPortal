from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView
# Create your views here.
class NewsList(ListView):

    model = Post
    ordering = "-time_of_creation" #"post_raiting"
    #queryset = Post.objects.order_by('-post_rating')
    # Имя файла шаблона(как представить объекты)
    template_name = "news.html"
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = "news"

class NewsDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — new.html
    template_name = 'new.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'new'
    #pk_url_kwarg = "id"