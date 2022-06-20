from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    # path('products/', views.products),
    path('customer/', views.display_all_images, name="products"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('user/', views.userPage, name="user"),
    path('send-image/', views.sendImage, name="send-image"),
    path('userlist/', views.userList, name="userList"),
]