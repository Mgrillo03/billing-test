from unicodedata import name
from . import views

from django.urls import path

app_name = 'accounts'

urlpatterns = [
    #/user-id/account/home/
    path('home/', views.index, name='index'),

    #----------- Accounts -----------#
    #/user-id/acoount/new/
    path('new/', views.create_account, name='create_account'),
    #/user-id/account/created
    path('created/', views.create_account_save, name='account_created'),

    #/user-id/account/account-id/detail/
    path('<int:account_id>/detail', views.account_detail, name='account_detail'),
    
    #user-id/account/account-id/update
    path('<int:account_id>/update/', views.update_account, name='update_account'),
    #user-id/account/account-id/update
    path('<int:account_id>/update-save/', views.update_account_save, name='account_updated'),

    #user-id/account/account-id/delete
    path('<int:account_id>/delete/', views.delete_account, name='delete_account'),
    #user-id/account/account-id/delete
    path('<int:account_id>/delete-success/', views.delete_account_save, name='account_deleted'),

    #----------- Operations -----------#
    ##  Create
    #/user-id/operation/new
    path('operation/new/', views.new_operation, name='new_operation'),
    #/user-id/opertion/created
    path('operation/created/', views.new_operation_save, name='operation_created'),
    #/user-id/operation/new-transfer
    path('operation/new-transfer/', views.new_operation_transfer, name='new_operation_transfer'),
    #/user-id/operation/transfer-created/
    path('operation/transfer-created/', views.new_transfer_save, name='transfer_created'),

    ##  Details
    #/user-id/operation/operation-id/detail/
    path('operation/<int:operation_id>/detail/', views.operation_detail, name='operation_detail'),

    ##  Update
    #user-id/operation/operation-id/update/
    path('operation/<int:operation_id>/update/', views.update_operation, name="update_operation"),
    #user-id/operation/operation-id/update-transfer/
    #path('operation/<int:operation_id>/update-transfer/', views.update_transfer, name="update_transfer"),
    #user-id/operation/operation-id/update-saved/
    path('operation/<int:operation_id>/update-saved/',views.update_operation_save, name='update_operation_save'),

    ##  Delete
    #user-id/operation/operation-id/confirm-delete/
    path('operation/<int:operation_id>/confirm-delete/', views.confirm_operation_delete, name='confirm_operation_delete'),
    #user-id/operation/operation-deleted/
    path('operation/<int:operation_id>/operation-deleted/', views.delete_operation, name='delete_operation'),

    #----------- Categories -----------#
    ## View 
    #category/
    path('category/',views.user_categories, name='user_categories'),
    
    ## Details
    #category/category_id/detail/
    path('category/<int:category_id>/detail/', views.category_detail, name='category_detail'),

    ## Create
    #category/new/
    path('category/new/', views.new_category, name='new_category'),
    #category/created/
    path('category/created/', views.new_category_save, name='new_category_save'),

    ## Update
    #category/category_id/update
    path('category/<int:category_id>/update', views.update_category, name='update_category'),
    #category/category_id/update-saved/
    path('category/<int:category_id>/update-saved/', views.update_category_save, name='update_category_save'),

    ## Delete
    #category/category_id/confirm-delete
    path('category/<int:category_id>/confirm-delete/', views.confirm_category_delete, name='confirm_category_delete'),
    #category/category_id/deleted/
    path('category/<int:category_id>/deleted/', views.delete_category, name='delete_category'),    


]