from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def reset_messages(request):
    try : 
        aux = request.session['message_shown']
    except KeyError:
        request.session['message_shown'] = False
        request.session['error_message'] = ''
        request.session['success_message'] = ''
        return request
    else:
        if not request.session['message_shown'] :
            request.session['message_shown'] = True
        else:
            request.session['error_message'] = ''
            request.session['success_message'] = ''
        return request

def check_username(username,list_users):
    """
    check if username is available in user list
    """    
    for i in list_users:
        if username == i.username:
            return False
    return True

def check_email(email, list_users):
    """
    check if email is available in user list
    """
    for i in list_users:
        if email == i.email:
            return False
    return True

def index(request):    
    request = reset_messages(request)
    list_users = User.objects.all()
    return render(request,'main/index.html',{
        'list_users' : list_users,
    })

def singup(request):
    request = reset_messages(request)
    return render(request,'main/singup.html',{})

def singup_next(request):
    list_users = User.objects.all()
    username = request.POST['username']
    username = username.lower()
    username_unique = check_username(username, list_users)
    email = request.POST['email']
    email_unique = check_email(email, list_users)
    password = request.POST['password']
    password_confirm = request.POST['confirm_password']

    
    if username_unique and email_unique and password == password_confirm:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user = User.objects.create(username=username, email=email, password=password, first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.save()   
        return render(request, 'main/singup_next.html',{})
    elif not username_unique: 
        request.session['error_message'] = f'El username {username} no esta disponible'
        request.session['message_shown'] = False
        return redirect('main:singup')
    elif not email_unique: 
        request.session['error_message'] = f'El email {email} no esta disponible'
        request.session['message_shown'] = False
        return redirect('main:singup')
    else: 
        request.session['error_message'] = 'Las contraseñas no coinciden'
        request.session['message_shown'] = False
        return redirect('main:singup')

@login_required
def user_main_view(request):
    request = reset_messages(request)
    user = User.objects.get(id=request.user.id)
    return render(request, 'main/main_view.html', {
        'user':user,
    })

def auth_login(request):
    if request.user.is_authenticated:
        return render(request, 'main/main_view.html',{})
    else:            
        request = reset_messages(request)
        return render(request, 'registration/login.html', {'message':'main'})

def auth_login_next(request):
    username = request.POST['username']
    username = username.lower()
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return user_main_view(request)
    else:
        request.session['error_message'] = 'El usuario y la contraseña no coinciden'
        request.session['message_shown'] = False
        return redirect('main:mylogin')
        

def auth_logout(request):
    logout(request)
    request = reset_messages(request)
    return render(request, 'registration/logout.html',{})

@login_required
def auth_reset_password(request):
    """
        Reset password using actual password
    """
    request = reset_messages(request)
    return render(request, 'registration/set_password.html',{})

@login_required
def auth_save_new_password(request):
    """
        Save change in new password
    """
    password = request.POST['actual_password']
    user = User.objects.get(id=request.user.id)

    if not user.check_password(password):
        request.session['error_message'] = 'La contraseña no es correcta'
        request.session['message_shown'] = False
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
            request.session['message_shown'] = False
            return redirect('main:reset_password')

@login_required
def update_user(request):
    user = User.objects.get(id=request.user.id)
    request = reset_messages(request)
    return render(request,'main/update_user.html',{'user':user})

@login_required
def update_user_save(request):
    list_users = User.objects.all().exclude(pk=request.user.id)
    new_username = request.POST['username']
    new_username = new_username.lower()
    username_unique = check_username(new_username, list_users)
    email = request.POST['email']
    email_unique = check_email(email, list_users)

   
    if username_unique and email_unique:
        user = User.objects.get(id=request.user.id)
        user.username = new_username
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = email
        user.save()
        request.session['success_message'] = 'Cambios guardados satisfactoriamente'
        request.session['message_shown'] = False
        return redirect('main:update_user')
    elif not username_unique: 
        request.session['error_message'] = f'El username {new_username} no esta disponible'
        request.session['message_shown'] = False
        return redirect('main:update_user')
    elif not email_unique:
        request.session['error_message'] = f'El email {email} no esta disponible'
        request.session['message_shown'] = False
        return redirect('main:update_user')

@login_required
def delete_user(request,user_id):
    request = reset_messages(request)
    return render(request, 'main/delete_user.html',{})

@login_required
def delete_user_save(request,user_id):
    user = User.objects.get(pk=user_id)
    password = request.POST['password']
    if user.check_password(password):
        logout(request)
        user.delete()
        request.session['success_message'] = 'Usuario eliminado satisfactoriamente'
        request.session['message_shown'] = False        
        return render(request, 'main/delete_user_saved.html',{})
    else:
        request.session['error_message'] = 'La contraseña es incorrecta'
        request.session['message_shown'] = False        
        return redirect('main:delete_user',user_id)

    


"""
manuel
clave: clave123

sirius
clave: sirius123

shari
clave: 12345678


"""