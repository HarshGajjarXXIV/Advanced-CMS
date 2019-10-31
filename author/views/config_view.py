from django.shortcuts import redirect
from blog.models import Configuration
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    UpdateView,
)


class ConfigUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Configuration
    fields = ['blog_name', 'blog_description', 'blog_logo',
              'display_copyright_notice', 'copyright_notice',
              'twitter_link', 'instagram_link', 'facebook_link',
              'display_about_us', 'about_us',
              'display_contact_us', 'contact_us',
              'display_privacy_policy', 'privacy_policy',
              'display_terms_of_service', 'terms_of_service',]
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