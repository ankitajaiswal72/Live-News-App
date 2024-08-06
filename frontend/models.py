from django.db import models
from django.contrib.auth.models import User
class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    region = models.CharField(max_length=255)
    language = models.CharField(max_length=50)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'article')