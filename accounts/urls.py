from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    # path('products/', views.products),
    path('customer/', views.display_all_images),
    # path('register/', views.registerPage, name="register"),
    # path('login/', views.loginPage, name="login"),
    # path('logout/', views.logoutUser, name="logout"),
]