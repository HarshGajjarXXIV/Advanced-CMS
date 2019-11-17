from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from author.forms import AuthorAddForm, AuthorAddGroupForm, AuthorProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)

from blog.models import Article, Comment


class AuthorList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    context_object_name = 'authors'
    template_name = 'author/author/author_list.html'

    def test_func(self):
        user = self.request.user
        if user.is_superuser \
                or user.has_perm('auth.view_user') \
                or user.has_perm('auth.add_user') \
                or user.has_perm('auth.change_user') \
                or user.has_perm('auth.delete_user'):
            return True
        else:
            return False

    def get_queryset(self):
        return User.objects.all()


class AuthorCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    template_name = 'author/author/author_create.html'
    form_class = AuthorAddForm

    def test_func(self):
        user = self.request.user
        if user.is_superuser or user.has_perm('auth.add_user'):
            return True
        else:
            return False

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'New Author added successfully')
        return redirect('author:author-list')


class PermissionsUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    context_object_name = 'author'
    template_name = 'author/author/author_permissions_update.html'
    form_class = AuthorAddGroupForm

    def test_func(self):
        user = self.get_object()
        logged_user = self.request.user
        if logged_user.is_superuser:
            return True
        elif logged_user.has_perm('auth.change_user') and not user.is_superuser:
            return True
        else:
            return False

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Admin\'s permissions has been updated!')
        return redirect('author:author-list')


class ProfileUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'author/author/profile_update.html'
    form_class = AuthorProfileUpdateForm

    def test_func(self):
        user = self.get_object()
        logged_user = self.request.user
        if user == logged_user:
            return True
        else:
            return False

    def get_form_kwargs(self):
        kwargs = super(ProfileUpdate, self).get_form_kwargs()
        kwargs.update(instance={
            'author': self.object,
            'profile': self.object.profile,
        })
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your profile has been updated!')
        return redirect('author:profile')


class AuthorDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    context_object_name = 'author'
    template_name = 'author/author/profile.html'

    def test_func(self):
        user = self.request.user
        if user.is_superuser or user.has_perm('auth.view_user'):
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super(AuthorDetail, self).get_context_data(**kwargs)

        if self.kwargs['pk']:
            author = User.objects.get(id=self.kwargs['pk'])
            articles = Article.objects.filter(author=author)
            comments = Comment.objects.filter(user_name=author).filter(email=author.email)
        else:
            articles = Article.objects.filter(author=self.request.user)
            comments = Comment.objects.filter(user_name=self.request.user).filter(email=self.request.user.email)

        context.update({
            'articles': articles,
            'comments': comments,
        })

        return context


class Profile(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    context_object_name = 'author'
    template_name = 'author/author/profile.html'

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        else:
            return False

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        articles = Article.objects.filter(author=self.request.user)
        comments = Comment.objects.filter(author=self.request.user)

        context.update({
            'articles': articles,
            'comments': comments,
        })

        return context


class AuthorDeactivate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User

    def test_func(self):
        user_to_deactivate = self.get_object()
        user = self.request.user
        if user.is_superuser or user == user_to_deactivate:
            return True
        elif user.has_perm('auth.delete_user') and not user_to_deactivate.is_superuser:
            return True
        else:
            return False

    def get(self, *args, **kwargs):
        user = get_object_or_404(User, id=self.kwargs['pk'])
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()

        if self.request.user == user:
            return redirect('author:login')
        else:
            return redirect('author:author-list')
