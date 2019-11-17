from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from blog.models import Comment
from blog.models import Article
from django.contrib import messages
from django.urls import reverse_lazy
from author.forms import ArticleAddForm, CommentAddForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


class Homepage(LoginRequiredMixin, ListView):
    context_object_name = 'articles'
    template_name = 'author/article/article_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.all().filter(author=self.request.user).filter(is_posted=True).order_by('-date_posted')


class ArticleAll(LoginRequiredMixin, ListView):
    context_object_name = 'articles'
    template_name = 'author/article/article_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(is_posted=True).order_by('-date_posted')


class ArticleDraft(LoginRequiredMixin, ListView):
    context_object_name = 'articles'
    template_name = 'author/article/article_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(is_posted=False).filter(author=self.request.user).order_by('-date_posted')


class ArticleFeatured(LoginRequiredMixin, UserPassesTestMixin, ListView):
    context_object_name = 'articles'
    template_name = 'author/article/article_list.html'
    paginate_by = 10

    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        else:
            return False

    def get_queryset(self):
        return Article.objects.filter(is_posted=True).filter(is_featured=True).order_by('-date_posted')


class ArticleCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = ArticleAddForm
    template_name = 'author/article/article_create.html'

    def test_func(self):
        user = self.request.user
        if user.is_superuser or user.has_perm('blog.add_article'):
            return True
        else:
            return False

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.ip_address = self.request.META['REMOTE_ADDR']

        if 'publish' in self.request.POST:
            form.instance.is_posted = True
            messages.success(self.request, '"Article" has been published successfully')
            return super().form_valid(form)

        if 'draft' in self.request.POST:
            form.instance.is_posted = False
            messages.success(self.request, '"Article" has been saved as draft')
            super().form_valid(form)
            return redirect('author:article-draft')


class ArticleUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleAddForm
    template_name = 'author/article/article_create.html'

    def test_func(self):
        article = self.get_object()
        user = self.request.user
        if user == article.author or user.is_superuser or user.has_perm('blog.change_article'):
            return True
        else:
            return False

    def form_valid(self, form):

        if 'publish' in self.request.POST:
            form.instance.is_posted = True
            messages.success(self.request, '"Article" has been updated successfully')
            return super().form_valid(form)

        if 'draft' in self.request.POST:
            form.instance.is_posted = False
            messages.success(self.request, '"Article" has been saved as draft')
            super().form_valid(form)
            return redirect('author:article-draft')


class ArticleDetail(LoginRequiredMixin, FormMixin, DetailView):
    form_class = CommentAddForm
    template_name = 'author/article/article_detail.html'

    def get_queryset(self):
        article = Article.objects.filter(id=self.kwargs['pk'])
        if article is None:
            raise Http404()
        else:
            return article

    def get_context_data(self, *args, **kwargs):
        temp_article = get_object_or_404(Article, id=self.kwargs['pk'])
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(article=temp_article, reply=None).order_by('-date_posted')
        context['form'] = self.get_form()
        return context

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            temp_article = get_object_or_404(Article, id=self.kwargs['pk'])
            reply_id = self.request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            form.instance.reply = comment_qs
            form.instance.article = temp_article
            form.instance.user_name = self.request.user
            form.instance.email = self.request.user.email
            form.instance.is_author = True
            form.instance.author = self.request.user
            form.instance.ip_address = self.request.META['REMOTE_ADDR']
            form.instance.is_approved = True
            form.save()
            messages.success(self.request, 'Your comment added successfully')
            return redirect(self.request.path)


class ArticleDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'author/article/article_confirm_delete.html'
    success_url = reverse_lazy('author:homepage')
    success_message = 'Article has been deleted successfully'

    def test_func(self):
        article = self.get_object()
        user = self.request.user
        if user == article.author or user.is_superuser or user.has_perm('blog.delete_article'):
            return True
        else:
            return False

    def delete(self, request, *args, **kwargs):
        messages.error(self.request, self.success_message)
        return super(ArticleDelete, self).delete(request, *args, **kwargs)


class CommentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'author/article/comment_confirm_delete.html'
    success_url = reverse_lazy('author:homepage')
    success_message = 'Comment has been deleted successfully'

    def test_func(self):
        comment = self.get_object()
        user = self.request.user
        if user == comment.author or user.is_superuser or user.has_perm('blog.delete_comment'):
            return True
        else:
            return False

    def delete(self, request, *args, **kwargs):
        messages.error(self.request, self.success_message)
        return super(CommentDelete, self).delete(request, *args, **kwargs)

