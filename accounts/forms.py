# YOUR OWN FORMS

from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TestImage


class ImageForm(forms.Form):
    image = forms.ImageField()


class CustomerImageForm(forms.Form):
    name = forms.CharField()
    image_field = forms.ImageField()


class UserTestImageForm(forms.ModelForm):
    class Meta:
        model = TestImage
        fields = ('image_name', 'image_field')


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ImageFromTextForm(forms.Form):
    user_id = forms.CharField()
    src = forms.CharField(widget=forms.HiddenInput())


class UploadedImageForm(forms.Form):
    user_id = forms.CharField()
    src = forms.ImageField()
