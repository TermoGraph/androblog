import hashlib

from django import forms

from .models import PublicUsers, Comment

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import ValidationError

class CreateUser(forms.ModelForm):
    

    class Meta:
        model = PublicUsers
        fields = ['username', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'for': "inputPassword"}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'for': "inputPassword"})
        }

        labels = {
            'username': ('Имя пользователя'),
            'password1': ('Пароль'),
            'password2': ('Повторите пароль')
        }

        error_messages = {
            'name': {
                'max_length': ("This writer name is too long."),
            }
        }

    def clean_username(self):
        new_username = self.cleaned_data['username'].lower()

        if PublicUsers.objects.filter(username__iexact=new_username).count():
            raise ValidationError('Имя пользователя {} уже существует'.format(new_username))
        return new_username

    def save(self):
        username = self.cleaned_data['username']
        password_one = self.cleaned_data['password1']
        password_two = self.cleaned_data['password2']

        if len(username) > 4:
            if password_one == password_two:
                new_user = PublicUsers.objects.create(
                    username=self.cleaned_data['username'],
                    password1=password_one,
                    password2=password_two
                )
                return new_user
            else:
                raise ValidationError('Пароли должны совпадать')
        else:
            raise ValidationError('Имя пользователя дольжен быть не менее больше 4 символов')


class LoginUser(forms.ModelForm):


    class Meta:
        model = PublicUsers
        fields = ['username', 'password1']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'for': "inputPassword"}),
        }

        labels = {
            'username': ('Имя пользователя'),
            'password1': ('Пароль'),
        }

        error_messages = {
            'name': {
                'max_length': ("This writer name is too long."),
            }
        }

class UserComments(forms.ModelForm):

    
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

        labels = {
            'text': ('Оставить коментарию')
        }

    def save(self, author, post_slug):
        text = self.cleaned_data['text']
        new_comm = Comment.objects.create(
            author=author,
            post_slug=post_slug,
            text=text)
        return new_comm