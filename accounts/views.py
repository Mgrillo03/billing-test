from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Account

def reset_messages(request):

    if not request.session['message_shown'] :
        request.session['message_shown'] = True
    else:
        request.session['error_message'] = ''
        request.session['success_message'] = ''
    return request

def check_account_name(name,list_users):
    """
    check if account name is available in users account list
    """    
    for i in list_users:
        if name == i.name:
            return False
    return True

@login_required
def index(request, user_id):
    ## Inicializar variables cuando se abre la pagina, no importa el link
    request.session['message_shown'] = False
    request = reset_messages(request)
    list_accounts = Account.objects.filter(user=request.user)

    if not request.session['message_shown'] :
        request.session['message_shown'] = True
    else:
        request.session['error_message'] = ''
        request.session['success_message'] = ''
    return render(request, 'accounts/index.html',{'list_accounts':list_accounts})

@login_required
def create_account(request, user_id):
    request = reset_messages(request)
    return render(request, 'accounts/create_account.html',{})

@login_required
def create_account_save(request,user_id):
    list_accounts = Account.objects.filter(user=request.user)
    name = request.POST['name']
    account_name_unique = check_account_name(name, list_accounts)

    if account_name_unique:
        initial_balance= float(request.POST['initial_balance'])
        description = request.POST['description']
        bank = request.POST['bank']
        user = User.objects.get(pk=request.user.id)
        account = Account.objects.create(name=name, description= description, balance = initial_balance, bank=bank, user=user)

        return render(request,'accounts/account_created.html',{'account':account})
    else:
        request.session['error_message'] = 'Ya tenes una cuenta con ese nombre'
        request.session['message_shown'] = False        
        return redirect('accounts:create_account',user_id)

@login_required
def update_account(request, user_id, account_id):
    account = Account.objects.get(id=account_id)
    request = reset_messages(request)
    return render(request,'accounts/update_account.html',{'account':account})

@login_required
def update_account_save(request, user_id, account_id):
    list_accounts = Account.objects.filter(user=request.user).exclude(pk=account_id)
    new_account_name = request.POST['name']
    account_name_unique = check_account_name(new_account_name, list_accounts)
   
    if account_name_unique :
        account = Account.objects.get(id=account_id)
        account.name = new_account_name
        account.description = request.POST['description']
        account.bank = request.POST['bank']
        ##account.balance = float(request.POST['balance']) 
        ### Para cambiar el balance mejor acerlo con operaciones
        account.save()
        request.session['success_message'] = 'Cambios guardados satisfactoriamente'
        request.session['message_shown'] = False
        return redirect('accounts:update_account', user_id, account_id)
    elif not account_name_unique: 
        request.session['error_message'] = f'El nombre {new_account_name} no esta disponible'
        request.session['message_shown'] = False
        return redirect('accounts:update_account', user_id, account_id)


@login_required
def delete_account(request,user_id,account_id):
    request = reset_messages(request)
    return render(request, 'accounts/delete_account.html',{'account_id':account_id})
    


@login_required
def delete_account_save(request,user_id,account_id):
    account = Account.objects.get(pk=account_id)
    account.delete()
    request.session['success_message'] = 'Cuenta eliminada satisfactoriamente'
    request.session['message_shown'] = False        
    return redirect('accounts:index',user_id)
