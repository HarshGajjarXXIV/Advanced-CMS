from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from author.forms import GroupForm, GroupAddForm, GroupDescription
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


class GroupList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Group
    context_object_name = 'groups'
    template_name = 'author/admin_group/group_list.html'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False

    def get_queryset(self):
        return Group.objects.all()


class GroupCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Group
    template_name = 'author/admin_group/group_create.html'
    form_class = GroupForm

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False

    def form_valid(self, form):
        # Save the group first, because the description needs a group before it can be saved.
        group = form['group'].save()
        description = form['description'].save(commit=False)
        description.group = group
        description.save()
        messages.success(self.request, 'New Group added successfully')
        return redirect('author:group-list')

class GroupUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Group
    template_name = 'author/admin_group/group_create.html'
    form_class = GroupForm

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False

    def get_form_kwargs(self):
        kwargs = super(GroupUpdate, self).get_form_kwargs()
        kwargs.update(instance={
            'group': self.object,
            'description': self.object.groupdescription,
        })
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'group Updated Successfully')
        return redirect('author:group-list')


class GroupDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Group
    template_name = 'author/admin_group/group_confirm_delete.html'
    success_url = reverse_lazy('author:group-list')
    success_message = 'Group has been deleted successfully'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False

    def delete(self, request, *args, **kwargs):
        messages.error(self.request, self.success_message)
        return super(GroupDelete, self).delete(self, *args, **kwargs)