from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def reset_messages(request):
    request.session['password_error'] = False
    request.session['error_message'] = ''
    return request

def index(request):    
    request = reset_messages(request)
    list_users = User.objects.all()
    return render(request,'main/index.html',{
        'list_users' : list_users,
    })

def singup(request):
    return render(request,'main/singup.html',{})

def singup_next(request):
    username = request.POST['username']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.create(username=username, email=email, password=password, first_name=first_name,last_name=last_name)
    user.set_password(password)
    user.save()   

    return render(request, 'main/singup_next.html',{})

@login_required
def main_view(request):
    return render(request, 'main/main_view.html', {})

def auth_login(request):
    if request.session['password_error'] == True:
        request.session['password_error'] = False
    else:
        request.session['error_message'] = ''
    return render(request, 'registration/login.html', {'message':'main'})

def auth_login_next(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        login(request, user)
        return render(request, 'main/main_view.html', {})
    else:
        request.session['error_message'] = 'El usuario y la contraseña no coinciden'
        request.session['password_error'] = True
        return redirect('main:mylogin')
        

def auth_logout(request):
    logout(request)
    request = reset_messages(request)
    return render(request, 'registration/logout.html',{})

def auth_reset_password(request):
    if request.session['password_error'] == True:
        request.session['password_error'] = False
    else:
        request.session['error_message'] = ''

    return render(request, 'registration/set_password.html',{})

def auth_save_new_password(request):
    username=request.POST['username']
    try:
        user = User.objects.get(username=username)#get_object_or_404(User, username=username)
    except (KeyError, User.DoesNotExist):
        request.session['error_message'] = 'El usuario no existe en la base de datos'
        request.session['password_error'] = True
        return redirect('main:reset_password')                
    else:
        new_password = request.POST['new_password']
        new_password2 = request.POST['new_password2']
        if new_password == new_password2:     
            user.set_password(new_password)
            user.save()
            return render(request,'registration/new_password_saved.html',{})
        else:
            request.session['error_message'] = 'las contraseñas no coinciden'
            request.session['password_error'] = True
            return redirect('main:reset_password')