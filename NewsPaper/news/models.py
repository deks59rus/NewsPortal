
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
#from django.db.models import Sum
from datetime import date


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    _author_rating = models.IntegerField(default=0, db_column='author_rating')

    def update_rating(self):
        posts_rating = 0
        comments_rating = 0
        posts_comments_rating = 0
        posts = Post.objects.filter(author_post=self)
        for p in posts:
            posts_rating += p.post_rating
        comments = Comment.objects.filter(user=self.authorUser)
        for c in comments:
            comments_rating += c.comment_rating
        posts_comments = Comment.objects.filter(post__author_post = self)
        for pc in posts_comments:
            posts_comments_rating += pc.comment_rating
        self._author_rating = posts_rating *3 + comments_rating + posts_comments_rating
        self.save()
    def __str__(self):
        return f'{self.authorUser}'

class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)
    def __str__(self):
        return f'{self.category_name.title()}'

class Post(models.Model):
    NEWS = 'NE'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )
    author_post = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_category = models.ManyToManyField(Category, through='PostCategory')

    post_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    post_name = models.CharField(max_length=255)
    post_content = models.TextField()
    post_rating = models.IntegerField(default=0)
    time_of_creation = models.DateTimeField(auto_now_add=True)
    def date_out(self):
        return  str(self.time_of_creation.strftime("%B %d, %Y")) + "\t"
    def preview(self):
        post_preview_with_rating = "{}... \tРейтинг поста: {}".format(str(self.post_content[0:123]), self.post_rating)
        post_preview = "{}... ".format(str(self.post_content[0:123]))
        return post_preview
    def show_comments(self):
        results = []
        comments = Comment.objects.filter(post=self.id)
        for comm in comments:
            author = comm.user.username
            text = comm.comment_text
            results.append(f"{author} говорит: '{text}'")
        return results
    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()
    def __str__(self):
        return f'{self.post_name.title()}: {self.preview()}'
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.post.post_name.title()}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
    def __str__(self):
        return f'Комментарий к посту {self.post.post_name.title()} от пользователя {self.user} - {self.comment_date}'
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])