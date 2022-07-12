from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class RegisterForm(UserCreationForm):
    """ Форма регистрации """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    first_name = forms.CharField(required=False, help_text='Имя')
    last_name = forms.CharField(required=False, help_text='Фамилия')
    email = forms.EmailField(required=False, help_text='email')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
