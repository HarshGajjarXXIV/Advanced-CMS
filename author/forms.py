from django import forms
from django.contrib.auth.models import User
from .models import Profile
from blog.models import Article, Comment, Menu, SubMenu, Category
from django.contrib.auth.forms import UserCreationForm


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
