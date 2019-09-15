from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from author.forms import AuthorAddForm, AuthorUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from blog.models import Article, Comment


class AuthorList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    context_object_name = 'authors'
    template_name = 'author/author/author_list.html'

    def test_func(self):
        if self.request.user.is_superuser:
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
        if self.request.user.is_superuser:
            return True
        else:
            return False

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'New Author added successfully')
        return redirect('author:author-list')


class AuthorDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    context_object_name = 'author'
    template_name = 'author/author/profile.html'

    def test_func(self):
        if self.request.user.is_superuser:
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


@login_required
def edit_profile(request):
    if request.method == 'POST':
        author_form = AuthorUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if author_form.is_valid() and profile_form.is_valid():
            author_form.save()
            profile_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('author:profile')

    else:
        author_form = AuthorUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'author_form': author_form,
        'profile_form': profile_form
    }
    return render(request, 'author/author/profile_update.html', context)


class AuthorDeactivate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User

    def test_func(self):
        user_to_deactivate = self.get_object()
        user = self.request.user
        if user.is_superuser or user == user_to_deactivate:
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


# class ProfileUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Profile
#     template_name = 'author/author/profile_update.html'
#     form_class = {
#         AuthorUpdateForm,
#         ProfileUpdateForm
#     }
#
#     success_url = reverse_lazy('author:profile')
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#     def test_func(self):
#         if self.request.user.is_superuser:
#             return True
#         else:
#             return False
#
#     def form_valid(self, form):
#         form.save()
#         messages.success(self.request, 'Profile has been updated successfully')