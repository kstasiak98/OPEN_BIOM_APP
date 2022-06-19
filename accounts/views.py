from django.shortcuts import render, redirect
from .forms import CustomerImageForm, CreateUserForm, ImageFromTextForm, UserTestImageForm, ImageForm
from .models import *

# Create your views here.

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt

from .decorators import unauthenticated_user, allowed_user, admin_only

from accounts.EigenFaces.recognize import predict_user
import cv2
import numpy as np
import base64

#picture_admins

@login_required(login_url='login')
def display_all_images(request):

        image = CustomerImage.objects.all()

        return render(request, 'accounts/customer_images.html',
                     {'image_list' : image})


@login_required(login_url='login')
@admin_only
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
    else:
        form = CustomerImageForm()
    context['form'] = form
    return render(request,'accounts/dashboard.html', context)


@unauthenticated_user
def register(request):

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name="users")
            user.groups.add(group)

            messages.success(request, 'Account was created for '+ username)



            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user =authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username or Password is incorrect")

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def userPage(request):
    context = {}

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            name = "TEST"
            img_obj = form.cleaned_data.get("image")
            print("Poszło")
            print(img_obj)
            test_img = cv2.imread("/uploads/test/test3.jpg")
            print(predict_user(1, test_img))
            return render(request, 'accounts/user.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, 'accounts/user.html', {'form': form})


@unauthenticated_user
def sendImage(request):
    print(request.method)
    if request.method == 'POST':
        form = ImageFromTextForm(request.POST, request.FILES)
        if form.is_valid():
            src = form.cleaned_data.get("src")
            user_id = form.cleaned_data.get("user_id")
            img = data_uri_to_cv2_img(src)
            # prediction = predict_user(user_id, img)
            # if [i for i in prediction if i[1] < 100000]:
            #     login_user_as(user_id)
    else:
        form = ImageFromTextForm()
    return render(request, 'accounts/take_picture.html', {'form': form})


def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img