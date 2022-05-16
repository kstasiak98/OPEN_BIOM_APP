from django import forms


class CustomerImageForm(forms.Form):
    name = forms.CharField()
    image_field = forms.ImageField()