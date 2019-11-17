from django.urls import reverse_lazy
from blog.models import Message
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView
)


class MessageList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    context_object_name = 'user_messages'
    template_name = 'author/message/message_list.html'

    def test_func(self):
        user = self.request.user
        if user.is_superuser or user.has_perm('blog.view_message'):
            return True
        else:
            return False

    def get_queryset(self):
        return Message.objects.all().order_by('-date_posted')


class MessageDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Message
    context_object_name = 'user_message'
    template_name = 'author/message/message_detail.html'

    def test_func(self):
        user = self.request.user
        if user.is_superuser or user.has_perm('blog.view_message'):
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        data = super(MessageDetail, self).get_context_data(**kwargs)
        self.object.is_seen = True
        self.object.save()
        return data


class MessageDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    template_name = 'author/message/message_delete_confirm.html'
    success_url = reverse_lazy('author:message-list')
    success_message = 'Message has been deleted successfully'

    def test_func(self):
        user = self.request.user
        if user.is_superuser or user.has_perm('blog.delete_message'):
            return True
        else:
            return False

    def delete(self, request, *args, **kwargs):
        messages.error(self.request, self.success_message)
        return super(MessageDelete, self).delete(self, *args, **kwargs)
