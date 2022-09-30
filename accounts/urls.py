from . import views

from django.urls import path

app_name = 'accounts'

urlpatterns = [
    #/user-id/account/home/
    path('home/', views.index, name='index'),
    #/user-id/acoount/new/
    path('new/', views.create_account, name='create_account'),
    #/user-id/account/created
    path('created/', views.create_account_save, name='account_created'),
    

]