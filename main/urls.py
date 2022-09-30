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

    #main/login/
    path('login/', views.auth_login, name='mylogin'),
    #main/login/next
    path('login/next/', views.auth_login_next, name='login_next'),


    #main/view/
    path('<int:user_id>/', views.user_main_view, name='main_view'),
    #main/user_id/updeate
    path('<int:user_id>/update/', views.update_user, name='update_user'),
    #main/user_id/success
    path('<int:user_id>/update-saved/', views.update_user_save, name='update_user_save'),

    #main/logout
    path('logout/', views.auth_logout, name='logout'),

    #main/reset-password/
    path('reset-password/', views.auth_reset_password, name='reset_password'),
    #main/reset-password/success
    path('new-password/success/', views.auth_save_new_password, name='save_new_password'),

    #main/delete-user/
    path('<int:user_id>/delete-user/', views.delete_user, name='delete_user'),
    #main/delete-user/
    path('<int:user_id>/user-deleted/', views.delete_user_save, name='user_deleted'),
    
]