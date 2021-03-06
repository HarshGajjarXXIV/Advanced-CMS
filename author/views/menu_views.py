from blog.models import Menu, SubMenu
from django.contrib import messages
from django.urls import reverse_lazy
from author.forms import MenuAddForm, SubMenuAddForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)


class MenuList(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Menu
    context_object_name = 'menus'
    template_name = 'author/menu/menu_list.html'

    def test_func(self):
        user = self.request.user
        if user.is_superuser \
                or user.has_perm('blog.view_menu') \
                or user.has_perm('blog.add_menu') \
                or user.has_perm('blog.change_menu') \
                or user.has_perm('blog.delete_menu') \
                or user.has_perm('blog.view_submenu') \
                or user.has_perm('blog.add_submenu') \
                or user.has_perm('blog.change_submenu') \
                or user.has_perm('blog.delete_submenu'):
            return True
        else:
            return False

    def get_queryset(self):
        menus = Menu.objects.all()
        return menus

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MenuList, self).get_context_data(**kwargs)
        sub_menus = SubMenu.objects.all()
        context.update({
            'sub_menus': sub_menus
        })
        return context


class MenuCreate(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    form_class = MenuAddForm
    template_name = 'author/menu/menu_create.html'
    success_url = reverse_lazy('author:menu-list')

    def test_func(self):
        user = self.request.user
        if user.is_superuser or user.has_perm('blog.add_menu'):
            return True
        else:
            return False

    def form_valid(self, form):

        if form.instance.type == 'Category':
            if not form.instance.category_link:
                messages.error(self.request, 'Select valid category')
                return super().form_invalid(form)
            else:
                form.instance.article_link = None
                form.instance.author_link = None
                form.instance.external_url = None

        elif form.instance.type == 'Article':
            if not form.instance.article_link:
                messages.error(self.request, 'Select valid article')
                return super().form_invalid(form)
            else:
                form.instance.category_link = None
                form.instance.author_link = None
                form.instance.external_url = None

        elif form.instance.type == 'Author':
            if not form.instance.author_link:
                messages.error(self.request, 'Select valid author')
                return super().form_invalid(form)
            else:
                form.instance.article_link = None
                form.instance.category_link = None
                form.instance.external_url = None

        elif form.instance.type == 'URL':
            if not form.instance.external_url:
                messages.error(self.request, 'Enter valid url')
                return super().form_invalid(form)
            else:
                form.instance.article_link = None
                form.instance.author_link = None
                form.instance.category_link = None

        messages.success(self.request, 'New menu added successfully')
        return super().form_valid(form)


class MenuUpdate(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Menu
    form_class = MenuAddForm
    success_url = reverse_lazy('author:menu-list')
    template_name = 'author/menu/menu_create.html'

    def test_func(self):
        user = self.request.user
        if user.is_superuser or user.has_perm('blog.change_menu'):
            return True
        else:
            return False

    def form_valid(self, form):

        if form.instance.type == 'Category':
            if not form.instance.category_link:
                messages.error(self.request, 'Select valid category')
                return super().form_invalid(form)
            else:
                form.instance.article_link = None
                form.instance.author_link = None
                form.instance.external_url = None

        elif form.instance.type == 'Article':
            if not form.instance.article_link:
                messages.error(self.request, 'Select valid article')
                return super().form_invalid(form)
            else:
                form.instance.category_link = None
                form.instance.author_link = None
                form.instance.external_url = None

        elif form.instance.type == 'Author':
            if not form.instance.author_link:
                messages.error(self.request, 'Select valid author')
                return super().form_invalid(form)
            else:
                form.instance.article_link = None
                form.instance.category_link = None
                form.instance.external_url = None

        elif form.instance.type == 'URL':
            if not form.instance.external_url:
                messages.error(self.request, 'Enter valid url')
                return super().form_invalid(form)
            else:
                form.instance.article_link = None
                form.instance.author_link = None
                form.instance.category_link = None

        messages.success(self.request, 'Menu updated successfully')
        return super().form_valid(form)


class MenuDelete(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Menu
    template_name = 'author/menu/menu_confirm_delete.html'
    success_url = reverse_lazy('author:menu-list')
    success_message = 'Menu has been deleted successfully'

    def test_func(self):
        user = self.request.user
        if user.is_superuser or user.has_perm('blog.delete_menu'):
            return True
        else:
            return False

    def delete(self, request, *args, **kwargs):
        messages.error(self.request, self.success_message)
        return super(MenuDelete, self).delete(self, *args, **kwargs)


class SubMenuCreate(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    form_class = SubMenuAddForm
    success_url = reverse_lazy('author:menu-list')
    template_name = 'author/menu/menu_create.html'

    def test_func(self):
        user = self.request.user
        if user.is_superuser or user.has_perm('blog.add_submenu'):
            return True
        else:
            return False

    def form_valid(self, form):

        if form.instance.type == 'Category':
            if not form.instance.category_link:
                messages.error(self.request, 'Select valid category')
                return super().form_invalid(form)
            else:
                form.instance.article_link = None
                form.instance.author_link = None
                form.instance.external_url = None

        elif form.instance.type == 'Article':
            if not form.instance.article_link:
                messages.error(self.request, 'Select valid article')
                return super().form_invalid(form)
            else:
                form.instance.category_link = None
                form.instance.author_link = None
                form.instance.external_url = None

        elif form.instance.type == 'Author':
            if not form.instance.author_link:
                messages.error(self.request, 'Select valid author')
                return super().form_invalid(form)
            else:
                form.instance.article_link = None
                form.instance.category_link = None
                form.instance.external_url = None

        elif form.instance.type == 'URL':
            if not form.instance.external_url:
                messages.error(self.request, 'Enter valid url')
                return super().form_invalid(form)
            else:
                form.instance.article_link = None
                form.instance.author_link = None
                form.instance.category_link = None

        messages.success(self.request, 'New menu added successfully')
        return super().form_valid(form)


class SubMenuUpdate(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = SubMenu
    form_class = SubMenuAddForm
    success_url = reverse_lazy('author:menu-list')
    template_name = 'author/menu/menu_create.html'

    def test_func(self):
        user = self.request.user
        if user.is_superuser or user.has_perm('blog.change_submenu'):
            return True
        else:
            return False

    def form_valid(self, form):

        if form.instance.type == 'Category':
            if not form.instance.category_link:
                messages.error(self.request, 'Select valid category')
                return super().form_invalid(form)
            else:
                form.instance.article_link = None
                form.instance.author_link = None
                form.instance.external_url = None

        elif form.instance.type == 'Article':
            if not form.instance.article_link:
                messages.error(self.request, 'Select valid article')
                return super().form_invalid(form)
            else:
                form.instance.category_link = None
                form.instance.author_link = None
                form.instance.external_url = None

        elif form.instance.type == 'Author':
            if not form.instance.author_link:
                messages.error(self.request, 'Select valid author')
                return super().form_invalid(form)
            else:
                form.instance.article_link = None
                form.instance.category_link = None
                form.instance.external_url = None

        elif form.instance.type == 'URL':
            if not form.instance.external_url:
                messages.error(self.request, 'Enter valid url')
                return super().form_invalid(form)
            else:
                form.instance.article_link = None
                form.instance.author_link = None
                form.instance.category_link = None

        messages.success(self.request, 'Menu updated successfully')
        return super().form_valid(form)


class SubMenuDelete(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = SubMenu
    template_name = 'author/menu/menu_confirm_delete.html'
    success_url = reverse_lazy('author:menu-list')
    success_message = 'Sub-Menu has been deleted successfully'

    def test_func(self):
        user = self.request.user
        if user.is_superuser or user.has_perm('blog.delete_submenu'):
            return True
        else:
            return False

    def delete(self, request, *args, **kwargs):
        messages.error(self.request, self.success_message)
        return super(SubMenuDelete, self).delete(self, *args, **kwargs)