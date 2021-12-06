from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('user/', views.user, name="user"),
    path('home/', views.home, name="home"),
    path('admins/', views.adminHome, name="admins"),
    path('newdepto/', views.newdepto, name="newdepto"),
    path('edepto/', views.edepto, name="edepto"),
    path('func/', views.funcHome, name="func"),
    path('checkin/', views.checkin, name="checkin"),
    path('check/', views.check, name="check"),
    path('checker/', views.checker, name="checker"),
    path('checkout/', views.checkout, name="checkout"),
    path('register/', views.registerPage, name="register"),
    path('registerfunc/', views.registerFunc, name="registerfunc"),
    path('pswd/', views.pswd, name="pswd"),
    path('arriendo/', views.arriendo,name="arriendo"),
    path('editar/', views.editar,name="editar"),
    path('', include('pwa.urls')),
]
