from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from accounts.models import Operation_ac 
from .models import Category

def reset_messages(request):
    try : 
        aux = request.session['message_shown']
    except KeyError:
        request.session['message_shown'] = False
        request.session['error_message'] = ''
        request.session['success_message'] = ''
    else:
        if not request.session['message_shown'] :
            request.session['message_shown'] = True
        else:
            request.session['error_message'] = ''
            request.session['success_message'] = ''
        return request

def check_name(name,list):
    """
    check if account name is available in users account list
    """    
    for i in list:
        if name.lower() == i.name.lower():
            return False
    return True

@login_required
def user_categories(request):
    categories_income_list = Category.objects.filter(user=request.user,type='Income').order_by('name')
    categories_expense_list = Category.objects.filter(user=request.user,type='Expense').order_by('name')
    request = reset_messages(request)
    return render(request, 'categories/user_categories.html',{
        'categories_income_list': categories_income_list,
        'categories_expense_list': categories_expense_list,

    })
    
@login_required
def category_detail(request, category_id):
    try:
        category= Category.objects.get(pk=category_id)
    except (KeyError, Category.DoesNotExist):
        request = reset_messages(request)
        request.session['error_message'] = 'No se encontro la operacion selccionada'
        request.session['message_shown'] = False
        return redirect('accounts:index')
    else:
        request = reset_messages(request)
        operations_list = Operation_ac.objects.filter(category=category)
        total=0
        for operation in operations_list:
            total += operation.amount

        return render(request, 'categories/category_detail.html',{
            'category': category,
            'total':total,
        })

@login_required
def new_category(request):
    request = reset_messages(request)
    return render(request, 'categories/new_category.html',{})

@login_required
def new_category_save(request):
    categories_list = Category.objects.filter(user=request.user)
    name = request.POST['name']
    name_unique = check_name(name,categories_list)
    type = request.POST['type']
    print(type)
    if name_unique:
        #Category.objects.create(name=name, user=request.user, type=type)
        request.session['success_message'] = 'Categoria creada satisfactoriamente'
        request.session['message_shown'] = False
        return redirect('accounts:index')
    else:
        request = reset_messages(request)
        request.session['error_message'] = 'Ya existe una categoria con ese nombre'
        request.session['message_shown'] = False
        return redirect('accounts:new_category')

@login_required
def update_category(request, category_id):
    request = reset_messages(request)
    try:
        category = Category.objects.get(pk=category_id)
    except (KeyError, Category.DoesNotExist):
        request.session['error_message'] = 'No se encontro la categoria'
        request.session['message_shown'] = False
        return redirect('accounts:index')
    else: 
        return render(request, 'categories/update_category.html',{
            'category':category,
        })

@login_required
def update_category_save(request,category_id):
    try:
        category = Category.objects.get(pk=category_id)
    except (KeyError, Category.DoesNotExist):
        request.session['error_message'] = 'No se encontro la categoria'
        request.session['message_shown'] = False
        return redirect('accounts:index')
    else:         
        if category.name != 'Otros':
            categories_list = Category.objects.filter(user=request.user, type=category.type).exclude(pk=category_id)
            new_name = request.POST['name']
            name_unique = check_name(new_name,categories_list)
            if name_unique:
                category.name = new_name
                category.save()
                request.session['success_message'] = 'Cambios guardados satisfactoriamente'
                request.session['message_shown'] = False
                return redirect('accounts:index')
            else:
                request = reset_messages(request)
                request.session['error_message'] = 'Ya existe una categoria con ese nombre'
                request.session['message_shown'] = False
                return redirect('accounts:update_category',category_id)
        else:
            request = reset_messages(request)
            request.session['error_message'] = 'No se puede modificar la categoria Otros'
            request.session['message_shown'] = False
            return redirect('accounts:user_categories')

@login_required
def confirm_category_delete(request, category_id):
    category = Category.objects.get(pk=category_id)
    request = reset_messages(request)
    return render(request, 'categories/confirm_category_delete.html',{
        'category': category,
    })

@login_required
def delete_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    
    if category.name != 'Otros':
        second_category = Category.objects.get(name='Otros', user=request.user,type=category.type)
        operations_list = Operation_ac.objects.filter(category=category)
        for operation in operations_list:
            operation.category = second_category
        category.delete()
        request.session['success_message'] = 'Categoria eliminada satisfactoriamente'
        request.session['message_shown'] = False
        return redirect('accounts:user_categories')
    else: 
        request = reset_messages(request)
        request.session['error_message'] = 'No se puede eliminar la categoria Otros'
        request.session['message_shown'] = False
        return redirect('accounts:user_categories')

