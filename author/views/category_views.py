from django.shortcuts import redirect
from blog.models import Category
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)


class CategoryList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    context_object_name = 'categories'
    template_name = 'author/category/category_list.html'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False

    def get_queryset(self):
        return Category.objects.all()


class CategoryCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = 'author/category/category_create.html'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'New Category Added Successfully')
        return redirect('author:category-list')


class CategoryUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['name']
    template_name = 'author/category/category_create.html'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Category Updated Successfully')
        return redirect('author:category-list')


class CategoryDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'author/category/category_confirm_delete.html'
    success_url = reverse_lazy('author:category-list')
    success_message = 'Category has been deleted successfully'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False

    def delete(self, request, *args, **kwargs):
        messages.error(self.request, self.success_message)
        return super(CategoryDelete, self).delete(self, *args, **kwargs)