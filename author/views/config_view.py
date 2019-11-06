from django.shortcuts import redirect
from blog.models import Configuration
from django.contrib import messages
from author.forms import ConfigForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    UpdateView,
)


class ConfigUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Configuration
    form_class = ConfigForm
    template_name = 'author/config/blog_configurations.html'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Configurations Updated Successfully')
        return redirect('author:homepage')