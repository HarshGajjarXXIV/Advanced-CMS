from django.urls import path
from . import views
from .views import ContactView

app_name = 'blog'

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('category/<slug:slug>/', views.ArticlesByCategory.as_view(), name='articles-by-category'),
    path('tag/<slug:slug>/', views.ArticlesByTag.as_view(), name='articles-by-tag'),
    path('author/<slug:slug>/', views.ArticlesByAuthor.as_view(), name='articles-by-author'),
    path('contact/', ContactView.as_view(), name='contact-us'),
    path('about/', views.AboutView.as_view(), name='about-us'),
    path('privacy-policy/', views.PrivacyView.as_view(), name='privacy-policy'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('<slug:slug>/', views.ArticleDetail.as_view(), name='article-detail'),
]
