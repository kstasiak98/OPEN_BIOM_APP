from django.shortcuts import render
from .forms import CustomerImageForm
from .models import *

# Create your views here.

# from django.contrib.auth.forms import UserCreationForm


def display_all_images(request):

        image = CustomerImage.objects.all()

        return render(request, 'accounts/customer_images.html',
                     {'image_list' : image})


def home(request):
    context = {}
    if request.method == "POST":
        form = CustomerImageForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            img = form.cleaned_data.get("image_field")
            obj = CustomerImage.objects.create(
                image_name=name,
                image_field=img
            )
            obj.save()
            print(obj)
    else:
        form = CustomerImageForm()
    context['form'] = form
    return render(request,'accounts/dashboard.html', context)




