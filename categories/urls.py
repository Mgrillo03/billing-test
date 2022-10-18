from . import views

from django.urls import path

app_name = 'categories'

urlpatterns = [
    ## View 
    #category/
    path('',views.user_categories, name='user_categories'),
    
    ## Details
    #category/category_id/detail/
    path('<str:category_id>/detail/', views.category_detail, name='category_detail'),

    ## Create
    #category/new/
    path('new/', views.new_category, name='new_category'),
    #category/created/
    path('created/', views.new_category_save, name='new_category_save'),

    ## Update
    #category/category_id/update
    path('<str:category_id>/update', views.update_category, name='update_category'),
    #category/category_id/update-saved/
    path('<str:category_id>/update-saved/', views.update_category_save, name='update_category_save'),

    ## Delete
    #category/category_id/confirm-delete
    path('<str:category_id>/confirm-delete/', views.confirm_category_delete, name='confirm_category_delete'),
    #category/category_id/deleted/
    path('<str:category_id>/deleted/', views.delete_category, name='delete_category'),    

]