from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from main import views as main_views


urlpatterns = [
    path('admin/', admin.site.urls),

    #main
    path('', main_views.index, name='index'),
    path('main/', include('main.urls')),

    #accounts
    path('accounts/', include('accounts.urls')),

    #categories
    path('category/', include('categories.urls')),
    
    #Password reset
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
