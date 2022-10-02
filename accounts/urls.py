from unicodedata import name
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

    #user-id/account/account-id/update
    path('<int:account_id>/update/', views.update_account, name='update_account'),
    #user-id/account/account-id/update
    path('<int:account_id>/update-save/', views.update_account_save, name='account_updated'),

    #user-id/account/account-id/delete
    path('<int:account_id>/delete/', views.delete_account, name='delete_account'),
    #user-id/account/account-id/delete
    path('<int:account_id>/delete-success/', views.delete_account_save, name='account_deleted'),
    

]