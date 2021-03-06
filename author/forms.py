from django import forms
from django.contrib.auth.models import User, Group, Permission
from .models import Profile, GroupDescription
from blog.models import Article, Comment, Menu, SubMenu, Configuration
from django.contrib.auth.forms import UserCreationForm
from betterforms.multiform import MultiModelForm


class ConfigForm(forms.ModelForm):

    class Meta:
        model = Configuration
        fields = ['blog_name', 'blog_description',
                  'display_copyright_notice', 'copyright_notice',
                  'twitter_link', 'instagram_link', 'facebook_link',
                  'display_about_us', 'about_us',
                  'display_contact_us', 'contact_us',
                  'display_privacy_policy', 'privacy_policy',
                  'display_terms_of_service', 'terms_of_service']


class ArticleAddForm(forms.ModelForm):

    thumbnail = forms.ImageField(
        label="Thumbnail (Crop thumbnail to <b>800x400</b> before uploading, Otherwise thumbnail may look weired!)")

    summary = forms.CharField(label='Summary (Max Length:160, For SEO)', max_length=160,
                              widget=forms.Textarea(
                                  attrs={'rows': '4'}
                              ))

    class Meta:
        model = Article
        fields = ['title', 'thumbnail', 'category', 'tags', 'is_featured', 'summary', 'body']


class GroupAddForm(forms.ModelForm):

    name = forms.CharField(label='Admin Group Name',
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Admin group name',
                                      'class': 'shadow',
                                      }
                               ))

    permissions = forms.ModelMultipleChoiceField(label='Permissions (Hold \'Ctrl\' to select multiple permissions)',
                                                 queryset=Permission.objects,
                                                 widget=forms.SelectMultiple(
                                                     attrs={'class': 'shadow',
                                                            'size': '10'
                                                            }
                                                ))

    class Meta:
        model = Group
        fields = ['name', 'permissions']


class GroupDescriptionForm(forms.ModelForm):

    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(
                                      attrs={'placeholder': 'Add admin group description',
                                             'class': 'shadow',
                                             'rows': '5'
                                             }
                                  ))

    class Meta:
        model = GroupDescription
        fields = ['description']


class GroupForm(MultiModelForm):

    form_classes = {
        'group': GroupAddForm,
        'description': GroupDescriptionForm,
    }


class AuthorAddForm(UserCreationForm):

    username = forms.CharField(label='Username',
                               widget=forms.TextInput(
                                  attrs={'placeholder': 'Username',
                                         'class': 'shadow',
                                         }
                               ))

    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(
                                   attrs={'placeholder': 'Email',
                                          'class': 'shadow',
                                          }
                             ))

    first_name = forms.CharField(label='First Name', required=True,
                                 widget=forms.TextInput(
                                      attrs={'placeholder': 'First Name',
                                             'class': 'shadow',
                                             }
                                 ))

    last_name = forms.CharField(label='Last Name', required=True,
                                widget=forms.TextInput(
                                      attrs={'placeholder': 'Last Name',
                                             'class': 'shadow',
                                             }
                                ))

    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(
                                     attrs={'placeholder': 'Password',
                                            'class': 'shadow',
                                            }
                                ))

    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput(
                                     attrs={'placeholder': 'Confirm Password',
                                            'class': 'shadow',
                                            }
                                ))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class AuthorAddGroupForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['groups', 'is_superuser', 'is_staff']


class AuthorUpdateForm(forms.ModelForm):

    username = forms.CharField(label='Username',
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'Username',
                                          'class': 'shadow',
                                          }
                               ))

    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(
                                 attrs={'placeholder': 'Email',
                                        'class': 'shadow',
                                        }
                             ))

    first_name = forms.CharField(label='First Name', required=True,
                                 widget=forms.TextInput(
                                      attrs={'placeholder': 'First Name',
                                             'class': 'shadow',
                                             }
                                 ))

    last_name = forms.CharField(label='Last Name', required=True,
                                widget=forms.TextInput(
                                     attrs={'placeholder': 'Last Name',
                                            'class': 'shadow',
                                            }
                                ))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):

    profile_pic = forms.ImageField(
        label="Profile Pic (Crop your image to <b>200x200</b> before uploading, Otherwise you may look weired!)")

    bio = forms.CharField(label='Bio (Max Length:260)', max_length=260, required=False,
                          widget=forms.Textarea(
                                  attrs={'placeholder': 'Bio (Max Length:260)',
                                         'class': 'shadow',
                                         'rows': '4',
                                         }
                          ))

    twitter = forms.CharField(label='Twitter (i.e. "https://twitter.com/username")',
                              max_length=150, required=False,
                              widget=forms.TextInput(
                                     attrs={'placeholder': 'Twitter',
                                            'class': 'shadow',
                                            }
                              ))

    instagram = forms.CharField(label='Instagram (i.e. "https://instagram.com/username")',
                                max_length=150, required=False,
                                widget=forms.TextInput(
                                     attrs={'placeholder': 'Instagram',
                                            'class': 'shadow',
                                            }
                                ))

    facebook = forms.CharField(label='Facebook (i.e. "https://facebook.com/username")',
                               max_length=150, required=False,
                               widget=forms.TextInput(
                                    attrs={'placeholder': 'Facebook',
                                           'class': 'shadow',
                                           }
                                ))

    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio', 'twitter', 'instagram', 'facebook']


class AuthorProfileUpdateForm(MultiModelForm):

    form_classes = {
        'author': AuthorUpdateForm,
        'profile': ProfileUpdateForm,
    }


class MenuAddForm(forms.ModelForm):

    external_url = forms.CharField(label='External URL',
                                   max_length=200, required=False,
                                   widget=forms.TextInput(
                                       attrs={'placeholder': 'External URL',
                                              'class': 'shadow'}
                                   ))

    class Meta:
        model = Menu
        fields = ['type', 'name', 'external_url', 'category_link', 'article_link', 'author_link']


class SubMenuAddForm(forms.ModelForm):

    external_url = forms.CharField(label='External URL',
                                   max_length=200, required=False,
                                   widget=forms.TextInput(
                                       attrs={'placeholder': 'External URL',
                                              'class': 'shadow'}
                                   ))

    class Meta:
        model = SubMenu
        fields = ['type', 'name', 'parent_menu', 'external_url', 'category_link', 'article_link', 'author_link']


class CommentAddForm(forms.ModelForm):

    comment = forms.CharField(label='', max_length=260,
                              widget=forms.Textarea(
                                  attrs={'placeholder': 'Comment',
                                         'class': 'shadow',
                                         'rows': '7',
                                         }
                              ))

    class Meta:
        model = Comment
        fields = ['comment']
