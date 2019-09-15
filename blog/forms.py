from django import forms
from .models import Comment, Message


class MessageAddForm(forms.ModelForm):

    subject = forms.CharField(max_length=150, label='',
                              widget=forms.TextInput(
                                  attrs={'placeholder': 'Subject',
                                         'class': 'shadow'
                                         }
                              ))
    email = forms.EmailField(label='',
                             widget=forms.EmailInput(
                                 attrs={'placeholder': 'Email',
                                        'class': 'shadow'
                                        }
                             ))
    website = forms.CharField(max_length=150, label='', required=False,
                              widget=forms.TextInput(
                                  attrs={'placeholder': 'Website (If any)',
                                         'class': 'shadow'
                                         }
                              ))
    message = forms.CharField(label='',
                              widget=forms.Textarea(
                                  attrs={'placeholder': 'Message',
                                         'class': 'shadow'
                                         }
                              ))

    class Meta:
        model = Message
        fields = ['subject', 'email', 'website', 'message']


class CommentAddForm(forms.ModelForm):

    user_name = forms.CharField(max_length=50, label='',
                                widget=forms.TextInput(
                                    attrs={'placeholder': 'User Name',
                                           'class': 'shadow'
                                           }
                                ))
    email = forms.EmailField(label='',
                             widget=forms.EmailInput(
                                 attrs={'placeholder': 'Email',
                                        'class': 'shadow'
                                        }
                             ))
    comment = forms.CharField(label='', max_length=260,
                              widget=forms.Textarea(
                                  attrs={'placeholder': 'Comment',
                                         'class': 'shadow',
                                         'rows': '7',
                                         }
                              ))

    class Meta:
        model = Comment
        fields = ['user_name', 'email', 'comment']