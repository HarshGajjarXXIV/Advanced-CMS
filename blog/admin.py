from django.contrib import admin
from .models import Article, Category, Message, Comment


# Register your models here.
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Message)
admin.site.register(Comment)