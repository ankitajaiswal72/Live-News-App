# admin.py
from django.contrib import admin
from .models import Article, Vote

admin.site.register(Article)
admin.site.register(Vote)
