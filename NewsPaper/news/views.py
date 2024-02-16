from django.shortcuts import render
from .models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .filters import NewsFilter
from .forms import NewForm, ArticleForm, CommentForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.shortcuts import redirect
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
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        # Возвращаем из функции отфильтрованный список товаров
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class NewsDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — new.html
    template_name = 'new.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'new'
    #pk_url_kwarg = "id"
class NewsListWithSearch(NewsList):
    template_name =  "news_search.html"
    #form_class=NewForm
class NewCreate(CreateView):
    form_class = NewForm
    model = Post
    template_name = 'new_edit.html'

    def form_valid(self, form):
        new = form.save(commit=False)
        new.post_type = Post.NEWS
        return super().form_valid(form)
class NewUpdate(UpdateView):
    form_class = NewForm
    model = Post
    template_name = 'new_edit.html'
    def form_valid(self, form):
        new = form.save(commit=False)
        new.post_type = Post.NEWS
        return super().form_valid(form)
class ArticleCreate(CreateView):
    form_class = ArticleForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        new = form.save(commit=False)
        new.post_type = Post.ARTICLE
        return super().form_valid(form)
class ArticleUpdate(NewUpdate):
    template_name = 'article_edit.html'
class NewDelete(DeleteView):
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('news_list')
class ArticleDelete(NewDelete):
    template_name = 'article_delete.html'
class CommentaryCreate(CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'comment_edit.html'

    def form_valid(self, form):
        import re
        comm = form.save(commit=False)

       # data =self.get_context_data()
        link = self.get_current_page_url()
        post_id=re.findall(r'\d+', link)[-1]
        comm.post = Post.objects.get(id = post_id)
        return super().form_valid(form)

    def get_current_page_url(self):
        """
        Returns the current page URL.
        """
        return self.request.build_absolute_uri()