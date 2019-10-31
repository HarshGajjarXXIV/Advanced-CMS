from django.contrib import admin
from .models import Article, Category, Message, Comment, Configuration, Menu, SubMenu


# Register your models here.
admin.site.register(Configuration)
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Menu)
admin.site.register(SubMenu)
admin.site.register(Comment)
admin.site.register(Message)
