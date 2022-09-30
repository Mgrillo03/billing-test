import imp
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Account, Operation_ac

@login_required
def index(request, user_id):
    list_accounts = Account.objects.all()
    return render(request, 'accounts/index.html',{'list_accounts':list_accounts})

@login_required
def create_account(request, user_id):
    return render(request, 'accounts/create_account.html',{})

@login_required
def create_account_save(request,user_id):
    initial_balance= float(request.POST['initial_balance'])
    name = request.POST['name']
    description = request.POST['description']
    bank = request.POST['bank']
    user = User.objects.get(pk=request.user.id)
    account = Account.objects.create(name=name, description= description, balance = initial_balance, bank=bank, user=user)

    return render(request,'accounts/account_created.html',{'account':account})
