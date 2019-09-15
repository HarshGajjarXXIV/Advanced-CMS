from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)


class Article(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)
    thumbnail = models.ImageField(upload_to='thumbnails')
    category = models.ManyToManyField(Category)
    tags = TaggableManager()
    author = models.ForeignKey(User, on_delete=models.SET(2))
    summary = models.TextField(max_length=160)
    body = RichTextUploadingField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    is_posted = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.summary

    def get_absolute_url(self):
        return reverse('author:article-detail', kwargs={'pk': self.pk})

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)

        super().save()
        img = Image.open(self.thumbnail.path)
        img = img.resize((800, 400))
        img.save(self.thumbnail.path)


class Menu(models.Model):

    TYPE = [
        ('Separator', 'Separator'),
        ('Category', 'Category'),
        ('Article', 'Article'),
        ('Author', 'Author'),
        ('URL', 'External URL')
    ]

    type = models.CharField(max_length=20, choices=TYPE, default='Separator')
    name = models.CharField(max_length=50)
    category_link = models.ForeignKey(Category, max_length=200, blank=True, null=True, on_delete=models.CASCADE)
    article_link = models.ForeignKey(Article, max_length=200, blank=True, null=True, on_delete=models.CASCADE)
    author_link = models.ForeignKey(User, max_length=200, blank=True, null=True, on_delete=models.CASCADE)
    external_url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class SubMenu(models.Model):

    TYPE = [
        ('Category', 'Category'),
        ('Article', 'Article'),
        ('Author', 'Author'),
        ('URL', 'External URL')
    ]

    type = models.CharField(max_length=20, choices=TYPE, default='Category')
    name = models.CharField(max_length=50)
    parent_menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    category_link = models.ForeignKey(Category, max_length=200, blank=True, null=True, on_delete=models.CASCADE)
    article_link = models.ForeignKey(Article, max_length=200, blank=True, null=True, on_delete=models.CASCADE)
    author_link = models.ForeignKey(User, max_length=200, blank=True, null=True, on_delete=models.CASCADE)
    external_url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50)
    email = models.EmailField()
    is_author = models.BooleanField(default=False)
    author = models.ForeignKey(User, null=True, on_delete=models.SET(2))
    ip_address = models.GenericIPAddressField(null=True)
    comment = models.TextField(max_length=260)
    reply = models.ForeignKey('self', null=True, related_name="replies", on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_name


class Message(models.Model):
    subject = models.CharField(max_length=150)
    email = models.EmailField()
    website = models.URLField(max_length=150, null=True, blank=True)
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True)
    is_seen = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    def snippet(self):
        return self.message[0:100] + '...'
