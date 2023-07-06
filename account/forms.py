from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User

class ChangePasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['password1', 'password2']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']