from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('user/', views.user, name="user"),
    path('home/', views.home, name="home"),
    path('register/', views.registerPage, name="register"),
    path('pswd/', views.pswd, name="pswd"),
    path('arriendo/', views.arriendo,name="arriendo"),
    path('editar/', views.editar,name="editar"),
    path('', include('pwa.urls')),
]
