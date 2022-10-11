from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Account, Operation_ac, Category

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

def check_account_name(name,list_users):
    """
    check if account name is available in users account list
    """    
    for i in list_users:
        if name.lower() == i.name.lower():
            return False
    return True

def get_general_balance(accounts_list):
    balance = 0
    for account in accounts_list:
        balance += account.balance
    return balance

@login_required
def index(request, user_id):
    accounts_list = Account.objects.filter(user=request.user)
    operations_list = Operation_ac.objects.filter(account__in=accounts_list).order_by('-created_at')
    general_balance = get_general_balance(accounts_list)
    request = reset_messages(request)
    return render(request, 'accounts/index.html',{
        'accounts_list':accounts_list,
        'operations_list': operations_list,
        'general_balance': general_balance,
    })

@login_required
def create_account(request, user_id):
    request = reset_messages(request)
    return render(request, 'accounts/new_account.html',{})

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
def account_detail(request, user_id, account_id):
    try:
        account = Account.objects.get(pk=account_id)
    except (KeyError, Account.DoesNotExist):
        request.session['error_message'] = 'No se encontro la cuenta'
        request.session['message_shown'] = False
        return redirect('accounts:index', user_id)
    else:
        operations_list = Operation_ac.objects.filter(account=account)
        return render(request, 'accounts/account_detail.html',{
            'account': account,
            'operations_list': operations_list,
        })

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
        balance = float(request.POST['balance']) 
        if abs(balance - account.balance) > 0.01 :        
            try:
                checked = request.POST["balance_checkbox"]
            except KeyError:
                #checkbox not checked  
                account.balance = balance
            else:
                #checkbox checked
                difference = account.balance - balance
                category = Category.objects.get(name='Otros',user=request.user)
                if difference > 0 :
                    #Generate Expense 
                    Operation_ac.objects.create(description="Ajuste cuenta", type="Expense", category=category, amount=difference, account=account)
                    account.balance -= difference
                else:
                    #Generate Income
                    Operation_ac.objects.create(description="Ajuste cuenta", type="Income", category=category, amount=abs(difference), account=account)
                    account.balance += abs(difference)

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

@login_required
def new_operation(request, user_id):
    request = reset_messages(request)
    accounts_list = Account.objects.filter(user=request.user)
    category_list = Category.objects.filter(user=request.user)
    return render(request, 'accounts/new_operation.html', {
        'accounts_list': accounts_list,
        'category_list': category_list,
    })

@login_required
def new_operation_save(request, user_id):
    """
    function to create a new operation
    first check that the account specified exists
    then check de type of operation
    if type of operation is an income it add the amount to the account balance

    if type of operation is an spense it take the amount from the account balance
    """
    try:
        account = Account.objects.get(name=request.POST['account_name'],user=request.user)
        category = Category.objects.get(name=request.POST['category'],user=request.user)
    except (KeyError):
        request.session['error_message'] = 'Por favor seleccione de la lista'
        request.session['message_shown'] = False
        return redirect('accounts:new_operation', user_id)
    else:
        amount = float(request.POST['amount'])
        type = request.POST['type']
        if type == 'Income':
            account.balance+= amount
            account.save()
            description = request.POST['description']
            Operation_ac.objects.create(description=description, type=type, category=category, amount=amount, account=account)
            request.session['success_message']='Ingreso agreado correctamente'
            request.session['message_shown']= False
            return redirect('accounts:index', user_id)
        elif type == 'Expense':
            account.balance-= amount
            account.save()
            description = request.POST['description']
            request.session['success_message']='Gasto agreado correctamente'
            request.session['message_shown']= False
            Operation_ac.objects.create(description=description, type=type, category=category, amount=amount, account=account)
            return redirect('accounts:index', user_id)

@login_required
def new_operation_transfer(request, user_id):
    request = reset_messages(request)
    accounts_list = Account.objects.filter(user=request.user)
    return render(request, 'accounts/new_transfer.html', {
        'accounts_list': accounts_list,
    })

@login_required
def new_transfer_save(request, user_id):
    """
        if the two accounts are diferents then

        it creates a two operations:        
        Expense: the first take the money from the first account 
        Income: the second get the money in to the second account
    """
    account = Account.objects.get(name=request.POST['account_name'],user=User.objects.get(pk=user_id))
    amount = float(request.POST['amount'])
    try:
        second_account = Account.objects.get(name=request.POST['second_account_name'],user=User.objects.get(pk=user_id))
    except (KeyError, Account.DoesNotExist):
        request.session['error_message'] = 'Por favor seleccione una cuenta de la lista'
        request.session['message_shown'] = False
        return redirect('accounts:index', user_id)
    else:
        if second_account != account:
            account.balance -= amount
            account.save()
            second_account.balance += amount
            second_account.save()
            description = f'{account.name} => {second_account.name}'
            description_2 = f'{second_account.name} <= {account.name}'
            operation_1 =Operation_ac.objects.create(description=description, type='Transfer-Expense', amount=amount, account=account)
            operation_2 =Operation_ac.objects.create(description=description_2, type='Transfer-Income', amount=amount, account=second_account, transfer_id = operation_1.pk)
            operation_1.transfer_id = operation_2.pk
            operation_1.save()
            request.session['success_message']='Transferencia creada correctamente'
            request.session['message_shown']= False
            return redirect('accounts:index', user_id)
        else: 
            request.session['error_message'] = 'Las cuentas no pueden ser iguales'
            request.session['message_shown'] = False
            return redirect('accounts:new_operation_transfer', user_id)

@login_required
def operation_detail(request, user_id, operation_id):
    try:
        operation = Operation_ac.objects.get(pk=operation_id)
    except (KeyError, Operation_ac.DoesNotExist):
        request.session['error_message'] = 'No se encontro la operacion selccionada'
        request.session['message_shown'] = False
        return redirect('accounts:index', user_id)
    else:
        request = reset_messages(request)
        return render(request, 'accounts/operation_detail.html',{
            'operation': operation,
        })

@login_required
def update_operation(request, user_id, operation_id):
    try:
        operation = Operation_ac.objects.get(pk=operation_id)
    except (KeyError, Operation_ac.DoesNotExist):
        request.session['error_message'] = 'No se encontro la operacion selccionada'
        request.session['message_shown'] = False
        return redirect('accounts:index', user_id)
    else:
        request = reset_messages(request)
        if 'Transfer' in operation.type:
            second_operation = Operation_ac.objects.get(pk=operation.transfer_id)
            return render(request, 'accounts/update_operation.html',{
                'operation': operation,
                'second_operation': second_operation,
            })
        else: 
            category_list = Category.objects.filter(user=request.user)
            return render(request, 'accounts/update_operation.html',{
                'operation': operation,
                'category_list': category_list,
            })

@login_required
def update_transfer(request, user_id, operation_id):
    try:
        operation = Operation_ac.objects.get(pk=operation_id)
    except (KeyError, Operation_ac.DoesNotExist):
        request.session['error_message'] = 'No se encontro la operacion selccionada'
        request.session['message_shown'] = False
        return redirect('accounts:index', user_id)
    else:
        request = reset_messages(request)
        return render(request, 'accounts/update_transfer.html',{
            'operation': operation,
        })
    
@login_required
def update_operation_save(request, user_id, operation_id):
    operation = Operation_ac.objects.get(pk=operation_id)
    account = Account.objects.get(pk=operation.account.pk)
    category = Category.objects.get(name=request.POST['category'], user=request.user)
    amount = float(request.POST['amount'])
    if operation.type == 'Income':
        account.balance -= operation.amount
        account.balance += amount
        account.save()
        operation.amount = amount
        operation.description = request.POST['description']
        operation.category = category
        operation.save()
        request.session['success_message']='Cambios guardados de manera exitosa'
        request.session['message_shown']= False
        return redirect('accounts:update_operation', user_id, operation_id)
    elif operation.type == 'Expense':
        account.balance += operation.amount
        account.balance -= amount
        account.save()
        operation.amount = amount
        operation.description = request.POST['description']
        operation.category = category
        operation.save()
        request.session['success_message']='Cambios guardados de manera exitosa'
        request.session['message_shown']= False
        return redirect('accounts:update_operation', user_id, operation_id)
    else:
        second_operation = Operation_ac.objects.get(pk=operation.transfer_id)
        second_account = Account.objects.get(pk=second_operation.account.pk)
        if operation.type == 'Transfer-Expense':
            #First account
            account.balance += operation.amount
            account.balance -= amount
            account.save()
            operation.amount = amount
            operation.save()
            #second account
            second_account.balance -= second_operation.amount
            second_account.balance += amount
            second_account.save()
            second_operation.amount = amount
            second_operation.save()
        else:
            #First account
            account.balance -= operation.amount
            account.balance += amount
            account.save()
            operation.amount = amount
            operation.save()
            #second account
            second_account.balance += second_operation.amount
            second_account.balance -= amount
            second_account.save()
            second_operation.amount = amount
            second_operation.save()
            return redirect('accounts:index', user_id)
        request.session['success_message']='Cambios guardados de manera exitosa'
        request.session['message_shown']= False
        return redirect('accounts:update_operation', user_id, operation_id)

@login_required
def confirm_operation_delete(request, user_id, operation_id):
    try:
        operation = Operation_ac.objects.get(pk=operation_id)
    except (KeyError, Operation_ac.DoesNotExist):
        request.session['error_message'] = 'No se encontro la operacion selccionada'
        request.session['message_shown'] = False
        return redirect('accounts:index', user_id)
    else:
        request = reset_messages(request)
        return render(request, 'accounts/confirm_delete.html',{
            'operation': operation,
        })

@login_required
def delete_operation(request, user_id, operation_id):
    try:
        operation = Operation_ac.objects.get(pk=operation_id)
    except (KeyError, Operation_ac.DoesNotExist):
        request.session['error_message'] = 'No se encontro la operacion selccionada'
        request.session['message_shown'] = False
        return redirect('accounts:index', user_id)
    else:
        if operation.type == 'Income':
            account = Account.objects.get(pk=operation.account.pk)
            account.balance -= operation.amount
            account.save()
            operation.delete()
            request.session['success_message']='Operacion eliminada exitosamente'
            request.session['message_shown']= False     

        elif operation.type == 'Expense':
            account = Account.objects.get(pk=operation.account.pk)
            account.balance += operation.amount
            account.save()
            operation.delete()
            request.session['success_message']='Operacion eliminada exitosamente'
            request.session['message_shown']= False  

        elif operation.type == 'Transfer-Expense':
            account = Account.objects.get(pk=operation.account.pk)
            account.balance += operation.amount
            account.save()
            second_operation = Operation_ac.objects.get(pk=operation.transfer_id)
            second_account = Account.objects.get(pk=second_operation.account.pk)
            second_account.balance -= operation.amount
            operation.delete()
            second_operation.delete()
            request.session['success_message']='Operacion eliminada exitosamente'
            request.session['message_shown']= False  

        elif operation.type == 'Transfer-Income':
            account = Account.objects.get(pk=operation.account.pk)
            account.balance -= operation.amount
            account.save()
            second_operation = Operation_ac.objects.get(pk=operation.transfer_id)
            second_account = Account.objects.get(pk=second_operation.account.pk)
            second_account.balance += operation.amount
            operation.delete()
            second_operation.delete()
            request.session['success_message']='Operacion eliminada exitosamente'
            request.session['message_shown']= False  
        return redirect('accounts:index', user_id)

