from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import NewUser

class CreateUserForm(ModelForm):
    "Creating User Form"
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = NewUser
        fields = ['first_name','last_name','email', 'username', 'password', 'is_superuser','is_manager','is_engineer','is_active','is_staff']
        #fields = '__all__'

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    "User Login Form"
    email = forms.EmailField(label='Email')
    password = forms.CharField(label= 'Password', widget=forms.PasswordInput())
