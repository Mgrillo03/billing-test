import imp
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from main import views as main_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.index, name='index'),
    path('main/', include('main.urls')),
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('accounts/', include('django.contrib.auth.urls'))

    #Password reset
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
