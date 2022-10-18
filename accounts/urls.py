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
    path('<str:account_id>/detail', views.account_detail, name='account_detail'),
    
    #user-id/account/account-id/update
    path('<str:account_id>/update/', views.update_account, name='update_account'),
    #user-id/account/account-id/update
    path('<str:account_id>/update-save/', views.update_account_save, name='account_updated'),

    #user-id/account/account-id/delete
    path('<str:account_id>/delete/', views.delete_account, name='delete_account'),
    #user-id/account/account-id/delete
    path('<str:account_id>/delete-success/', views.delete_account_save, name='account_deleted'),

    #----------- Operations -----------#
    ##  Create
    #/user-id/operation/new-income
    path('operation/new-income/', views.new_operation_income, name='new_operation_income'),
    #/user-id/operation/new-expense
    path('operation/new-expense/', views.new_operation_expense, name='new_operation_expense'),
    #/user-id/opertion/created
    path('operation/created/', views.new_operation_save, name='operation_created'),
    #/user-id/operation/new-transfer
    path('operation/new-transfer/', views.new_operation_transfer, name='new_operation_transfer'),
    #/user-id/operation/transfer-created/
    path('operation/transfer-created/', views.new_transfer_save, name='transfer_created'),

    ##  Details
    #/user-id/operation/operation-id/detail/
    path('operation/<str:operation_id>/detail/', views.operation_detail, name='operation_detail'),

    ##  Update
    #user-id/operation/operation-id/update/
    path('operation/<str:operation_id>/update/', views.update_operation, name="update_operation"),
    #user-id/operation/operation-id/update-transfer/
    #path('operation/<str:operation_id>/update-transfer/', views.update_transfer, name="update_transfer"),
    #user-id/operation/operation-id/update-saved/
    path('operation/<str:operation_id>/update-saved/',views.update_operation_save, name='update_operation_save'),

    ##  Delete
    #user-id/operation/operation-id/confirm-delete/
    path('operation/<str:operation_id>/confirm-delete/', views.confirm_operation_delete, name='confirm_operation_delete'),
    #user-id/operation/operation-deleted/
    path('operation/<str:operation_id>/operation-deleted/', views.delete_operation, name='delete_operation'),
    
]