from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Count, F
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import FormMixin
from taggit.models import Tag
from .models import Article, Comment, Category, Menu, SubMenu, Configuration
from django.contrib import messages
from .forms import CommentAddForm, MessageAddForm
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    TemplateView
)


class Homepage(ListView):
    context_object_name = 'articles'
    template_name = 'blog/article/homepage.html'

    def get_queryset(self):

        if 's' in self.request.GET:
            search_term = self.request.GET['s']

            articles = Article.objects.filter(Q(slug__icontains=search_term) |
                                              Q(title__icontains=search_term) |
                                              Q(category__slug__icontains=search_term) |
                                              Q(category__name__icontains=search_term) |
                                              Q(author__username__icontains=search_term) |
                                              Q(author__first_name__icontains=search_term) |
                                              Q(author__last_name__icontains=search_term) |
                                              Q(tags__name__icontains=search_term) |
                                              Q(date_posted__icontains=search_term)
                                              ).order_by('-date_posted').distinct()

        else:
            articles = Article.objects.filter(is_posted=True).order_by('-date_posted')

        paginator = Paginator(articles, 6)
        page = self.request.GET.get('page')

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        return articles

    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        config = Configuration.objects.first()
        menus = Menu.objects.annotate(sub_count=Count('submenu')).order_by('id')
        sub_menus = SubMenu.objects.all()
        categories = Category.objects.all()
        tags = Tag.objects.all().annotate(num_times=Count('article')).order_by('-num_times')[:50]
        featured_articles = Article.objects.filter(is_featured=True)[:5]
        context.update({
            'config': config,
            'categories': categories,
            'menus': menus,
            'sub_menus': sub_menus,
            'tags': tags,
            'featured_articles': featured_articles
        })
        return context


class ArticleDetail(FormMixin, DetailView):
    template_name = 'blog/article/article_detail.html'
    form_class = CommentAddForm

    def get_queryset(self):
        article = Article.objects.filter(slug=self.kwargs['slug']).filter(is_posted=True)

        if article is None:
            raise Http404()
        else:
            article.update(views=F('views')+1)
            return article

    def get_context_data(self, *args, **kwargs):
        temp_article = get_object_or_404(Article, slug=self.kwargs['slug'])
        context = super(ArticleDetail, self).get_context_data(**kwargs)

        config = Configuration.objects.first()
        menus = Menu.objects.annotate(sub_count=Count('submenu')).order_by('id')
        sub_menus = SubMenu.objects.all()
        comments = Comment.objects.filter(
            article=temp_article,
            reply=None,
            is_approved=True).order_by('-date_posted')
        form = self.get_form()
        categories = Category.objects.all()
        tags = Tag.objects.all().annotate(num_times=Count('article')).order_by('-num_times')[:50]
        featured_articles = Article.objects.filter(is_featured=True)[:5]

        context.update({
            'config': config,
            'menus': menus,
            'sub_menus': sub_menus,
            'comments': comments,
            'form': form,
            'categories': categories,
            'tags': tags,
            'featured_articles': featured_articles
        })

        return context

    def post(self, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            temp_article = get_object_or_404(Article, slug=self.kwargs['slug'])
            reply_id = self.request.POST.get('comment_id')
            comment_qs = None

            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)

            form.instance.reply = comment_qs
            form.instance.article = temp_article
            form.instance.is_approved = True
            form.instance.ip_address = self.request.META['REMOTE_ADDR']
            form.save()

            messages.success(self.request, 'Your comment added successfully')
            return redirect(self.request.path)


class ArticlesByCategory(ListView):
    context_object_name = 'articles'
    template_name = 'blog/article/articles_by_category.html'
    # paginate_by = 5

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        articles = Article.objects.filter(category__slug=category.slug).filter(is_posted=True).order_by('-date_posted')

        paginator = Paginator(articles, 6)
        page = self.request.GET.get('page')

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        return articles

    def get_context_data(self, **kwargs):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        context = super(ArticlesByCategory, self).get_context_data(**kwargs)

        config = Configuration.objects.first()
        categories = Category.objects.all()
        menus = Menu.objects.annotate(sub_count=Count('submenu')).order_by('id')
        sub_menus = SubMenu.objects.all()
        tags = Tag.objects.all().annotate(num_times=Count('article')).order_by('-num_times')[:50]
        featured_articles = Article.objects.filter(is_featured=True)[:5]
        context.update({
            'config': config,
            'category': category,
            'categories': categories,
            'menus': menus,
            'sub_menus': sub_menus,
            'tags': tags,
            'featured_articles': featured_articles
        })
        return context


class ArticlesByTag(ListView):
    context_object_name = 'articles'
    template_name = 'blog/article/articles_by_tag.html'
    # paginate_by = 5

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        articles = Article.objects.filter(tags__slug=tag.slug).filter(is_posted=True).order_by('-date_posted')

        paginator = Paginator(articles, 6)
        page = self.request.GET.get('page')

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        return articles

    def get_context_data(self, **kwargs):
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        context = super(ArticlesByTag, self).get_context_data(**kwargs)

        config = Configuration.objects.first()
        categories = Category.objects.all()
        menus = Menu.objects.annotate(sub_count=Count('submenu')).order_by('id')
        sub_menus = SubMenu.objects.all()
        tags = Tag.objects.all().annotate(num_times=Count('article')).order_by('-num_times')[:50]
        featured_articles = Article.objects.filter(is_featured=True)[:5]
        context.update({
            'config': config,
            'tag': tag,
            'categories': categories,
            'menus': menus,
            'sub_menus': sub_menus,
            'tags': tags,
            'featured_articles': featured_articles
        })
        return context


class ArticlesByAuthor(ListView):
    context_object_name = 'articles'
    template_name = 'blog/article/articles_by_author.html'
    # paginate_by = 5

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs['slug'])
        articles = Article.objects.filter(author__username=author.username).filter(is_posted=True).order_by('-date_posted')

        paginator = Paginator(articles, 6)
        page = self.request.GET.get('page')

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        return articles

    def get_context_data(self, **kwargs):
        context = super(ArticlesByAuthor, self).get_context_data(**kwargs)

        config = Configuration.objects.first()
        author = get_object_or_404(User, username=self.kwargs['slug'])
        comments = Comment.objects.filter(author__username=self.kwargs['slug'])
        categories = Category.objects.all()
        menus = Menu.objects.annotate(sub_count=Count('submenu')).order_by('id')
        sub_menus = SubMenu.objects.all()
        tags = Tag.objects.all().annotate(num_times=Count('article')).order_by('-num_times')[:50]
        featured_articles = Article.objects.filter(is_featured=True)[:5]
        context.update({
            'config': config,
            'author': author,
            'comments': comments,
            'categories': categories,
            'menus': menus,
            'sub_menus': sub_menus,
            'tags': tags,
            'featured_articles': featured_articles
        })
        return context


class AboutView(TemplateView):
    template_name = 'blog/about/about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)

        config = Configuration.objects.first()
        menus = Menu.objects.annotate(sub_count=Count('submenu')).order_by('id')
        sub_menus = SubMenu.objects.all()
        context.update({
            'config': config,
            'menus': menus,
            'sub_menus': sub_menus,
        })
        return context


class ContactView(CreateView):
    form_class = MessageAddForm
    template_name = 'blog/about/contact.html'

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)

        config = Configuration.objects.first()
        menus = Menu.objects.annotate(sub_count=Count('submenu')).order_by('id')
        sub_menus = SubMenu.objects.all()
        context.update({
            'config': config,
            'menus': menus,
            'sub_menus': sub_menus,
        })
        return context

    def form_valid(self, form):
        form.instance.ip_address = self.request.META['REMOTE_ADDR']  # get_ip(self.request)
        form.save()
        messages.success(self.request, 'Your message has been sent successfully')
        return redirect('blog:contact-us')


class PrivacyView(TemplateView):
    template_name = 'blog/about/privacy_policy.html'

    def get_context_data(self, **kwargs):
        context = super(PrivacyView, self).get_context_data(**kwargs)

        config = Configuration.objects.first()
        menus = Menu.objects.annotate(sub_count=Count('submenu')).order_by('id')
        sub_menus = SubMenu.objects.all()
        context.update({
            'config': config,
            'menus': menus,
            'sub_menus': sub_menus,
        })
        return context


class TermsView(TemplateView):
    template_name = 'blog/about/terms.html'

    def get_context_data(self, **kwargs):
        context = super(TermsView, self).get_context_data(**kwargs)

        config = Configuration.objects.first()
        menus = Menu.objects.annotate(sub_count=Count('submenu')).order_by('id')
        sub_menus = SubMenu.objects.all()
        context.update({
            'config': config,
            'menus': menus,
            'sub_menus': sub_menus,
        })
        return context