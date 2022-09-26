import re
from tabnanny import check
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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
def user_main_view(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'main/main_view.html', {
        'user':user,
    })

def auth_login(request):
    if request.user.is_authenticated:
        return render(request, 'main/main_view.html',{})
    else:            
        if request.session['password_error'] == True:
            request.session['password_error'] = False
        else:
            request.session['error_message'] = ''
        return render(request, 'registration/login.html', {'message':'main'})

def auth_login_next(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return user_main_view(request,user.id)
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
    password = request.POST['actual_password']
    user = User.objects.get(id=request.user.id)
    # try:
    #     password_checked=request.user.check_password(password) #user = User.objects.get(id=request.user.id)#get_object_or_404(User, username=username)
    # except (KeyError, User.DoesNotExist):
    #     request.session['error_message'] = 'La contraseña no es correcta'
    #     request.session['password_error'] = True
    #     return redirect('main:reset_password')                
    # else:
    if not user.check_password(password):
        request.session['error_message'] = 'La contraseña no es correcta'
        request.session['password_error'] = True
        return redirect('main:reset_password')
    else :
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

def prueba(request):
    pass


"""
manuel
clave: clave123

sirius
clave: sirius123

shari
clave: 12345678


"""