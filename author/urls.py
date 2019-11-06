from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'author'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='author/auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', views.Homepage.as_view(), name='homepage'),

    path('configs/<int:pk>/', views.ConfigUpdate.as_view(), name='config-update'),

    path('article/<int:pk>/', views.ArticleDetail.as_view(), name='article-detail'),
    path('article/all/', views.ArticleAll.as_view(), name='article-all'),
    path('article/add/', views.ArticleCreate.as_view(), name='article-create'),
    path('article/<int:pk>/update/', views.ArticleUpdate.as_view(), name='article-update'),
    path('article/<int:pk>/delete/', views.ArticleDelete.as_view(), name='article-delete'),
    path('article/draft/', views.ArticleDraft.as_view(), name='article-draft'),
    path('article/featured/', views.ArticleFeatured.as_view(), name='article-featured'),

    path('menu/', views.MenuList.as_view(), name='menu-list'),
    path('menu/add/', views.MenuCreate.as_view(), name='menu-create'),
    path('menu/<int:pk>/update/', views.MenuUpdate.as_view(), name='menu-update'),
    path('menu/<int:pk>/delete/', views.MenuDelete.as_view(), name='menu-delete'),

    path('submenu/add/', views.SubMenuCreate.as_view(), name='submenu-create'),
    path('submenu/<int:pk>/update/', views.SubMenuUpdate.as_view(), name='submenu-update'),
    path('submenu/<int:pk>/delete/', views.SubMenuDelete.as_view(), name='submenu-delete'),

    path('comment/<int:pk>/delete/', views.CommentDelete.as_view(), name='comment-delete'),

    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('categories/add/', views.CategoryCreate.as_view(), name='category-create'),
    path('categories/<int:pk>/update/', views.CategoryUpdate.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDelete.as_view(), name='category-delete'),

    path('authors/', views.AuthorList.as_view(), name='author-list'),
    path('authors/add/', views.AuthorCreate.as_view(), name='author-create'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('authors/<int:pk>/', views.AuthorDetail.as_view(), name='author-detail'),
    path('authors/<int:pk>/deactivate/', views.AuthorDeactivate.as_view(), name='author-deactivate'),
    path('profile/update/', views.edit_profile, name='profile-update'),
    # path('profile/edit/', views.ProfileUpdate.as_view(), name='profile-update'),

    path('groups/', views.GroupList.as_view(), name='group-list'),
    path('groups/add/', views.GroupCreate.as_view(), name='group-create'),
    path('groups/<int:pk>/delete/', views.GroupDelete.as_view(), name='group-delete'),
    path('groups/<int:pk>/update/', views.GroupUpdate.as_view(), name='group-update'),

    path('messages/', views.MessageList.as_view(), name='message-list'),
    path('messages/<int:pk>/', views.MessageDetail.as_view(), name='message-detail'),
    path('messages/<int:pk>/delete/', views.MessageDelete.as_view(), name='message-delete'),
]
