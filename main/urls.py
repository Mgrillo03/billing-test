from . import views

from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'main'

urlpatterns = [
    #main/
    path('', views.index, name='index'),
    #main/singup/
    path('singup/', views.singup, name='singup'),
    #main/singup/next/
    path('singup/next/', views.singup_next, name='singup_next'),
    #main/view/
    path('view/<int:user_id>', views.user_main_view, name='main_view'),
    #main/login/
    path('login/', views.auth_login, name='mylogin'),
    #main/login/next
    path('login/next/', views.auth_login_next, name='login_next'),
    #main/logout
    path('logout/', views.auth_logout, name='logout'),
    #main/reset-password/
    path('reset-password/', views.auth_reset_password, name='reset_password'),
    #main/reset-password/success
    path('new-password/success', views.auth_save_new_password, name='save_new_password'),
    
]