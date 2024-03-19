from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post, Comment,  Subscriber, Category #PostCategory,
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .filters import NewsFilter
from .forms import NewForm, ArticleForm, CommentForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # Декоратор проверки авторизации
from django.views.decorators.csrf import csrf_protect # защита доступа
from django.db.models import Exists, OuterRef

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
print(CACHE_TTL)

#Импорт задач для проверки асинхронного выполнения:
from django.views import View
from .tasks import printer

# Пример асинхронного выполнения задачи:
class IndexView(View):
    def get(self, request):
        #printer.delay(N=10) # Пример 1
        printer.apply_async([10], countdown=0) # Пример 2
        # printer.apply_async([10], eta = datetime.now() + timedelta(seconds=5))
        # последний, параметр выполнения — expires. Он служит для того, чтобы убирать задачу из очереди по прошествии какого-то времени.
        return HttpResponse('Hello!')

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

class NewsDetail(LoginRequiredMixin,DetailView):
    raise_exception = True
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — new.html
    template_name = 'new.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'new'
    #pk_url_kwarg = "id"
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        # Добавляем в контекст комментарии объекта
        context['comments'] = Comment.objects.filter(post = self.object).order_by("-comment_date")
        return context
class NewsListWithSearch(NewsList):
    template_name =  "news_search.html"
    #form_class=NewForm
class NewCreate(PermissionRequiredMixin,CreateView):
    permission_required = ('news.add_post',)
    form_class = NewForm
    model = Post
    template_name = 'new_edit.html'

    def form_valid(self, form):
        new = form.save(commit=False)
        new.post_type = Post.NEWS
        return super().form_valid(form)
class NewUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewForm
    model = Post
    template_name = 'new_edit.html'
    def form_valid(self, form):
        new = form.save(commit=False)
        new.post_type = Post.NEWS
        return super().form_valid(form)

class ArticleList(ListView):
    model = Post
    ordering = '-time_of_creation'
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 10

class ArticleCreate(NewCreate):
    permission_required = ('news.create_post',)
    form_class = ArticleForm
    #model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        new = form.save(commit=False)
        new.post_type = Post.ARTICLE
        return super().form_valid(form)
class ArticleUpdate(NewUpdate):
    permission_required = ('news.change_post',)
    form_class = ArticleForm
    template_name = 'article_edit.html'
    def form_valid(self, form):
        new = form.save(commit=False)
        new.post_type = Post.ARTICLE
        return super().form_valid(form)
class NewDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('news_list')
class ArticleDelete(NewDelete):
    permission_required = ('news.delete_post',)
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
@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('category_name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )