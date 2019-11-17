from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from author.forms import GroupForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)


class GroupList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Group
    context_object_name = 'groups'
    template_name = 'author/admin_group/group_list.html'

    def test_func(self):
        user = self.request.user
        if user.is_superuser \
                or user.has_perm('auth.view_group') \
                or user.has_perm('auth.add_group') \
                or user.has_perm('auth.change_group') \
                or user.has_perm('auth.delete_group'):
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
        user = self.request.user
        if user.is_superuser or user.has_perm('auth.add_group'):
            return True
        else:
            return False

    def form_valid(self, form):
        # Save the group first, because the description needs a group before it can be saved.
        group = form['group'].save()
        description = form['description'].save(commit=False)
        description.group = group
        description.save()
        messages.success(self.request, 'New admin group added successfully')
        return redirect('author:group-list')

class GroupUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Group
    template_name = 'author/admin_group/group_create.html'
    form_class = GroupForm

    def test_func(self):
        user = self.request.user
        if user.is_superuser or user.has_perm('auth.change_group'):
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
        messages.success(self.request, 'Admin group updated successfully')
        return redirect('author:group-list')


class GroupDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Group
    template_name = 'author/admin_group/group_confirm_delete.html'
    success_url = reverse_lazy('author:group-list')
    success_message = 'Group has been deleted successfully'

    def test_func(self):
        user = self.request.user
        if user.is_superuser or user.has_perm('auth.delete_group'):
            return True
        else:
            return False

    def delete(self, request, *args, **kwargs):
        messages.error(self.request, self.success_message)
        return super(GroupDelete, self).delete(self, *args, **kwargs)