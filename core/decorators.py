from django.http  import HttpResponse
from django.shortcuts import redirect

##Redirecciona a home si el usuario esta autenticado, si no, lo lleva a la página a la que se dirigia (ex. registrar)
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

#Autenticación en base a grupos de Django
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('home')
        return wrapper_func
    return decorator


#Permite solo a admins a acceder esta pagina | hack para evadir ciertos problemas
def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        if group == 'user':
            return redirect('home')
        if group == 'func':
            return redirect('func')
        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_func

#Permite solo a usuarios a acceder esta pagina | hack para evadir ciertos problemas
def user_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        if group == 'admin':
            return redirect('admins')
        if group == 'func':
            return redirect('func')
        if group == 'user':
            return view_func(request, *args, **kwargs)

    return wrapper_func

#Permite solo a funcionarios a acceder esta pagina | hack para evadir ciertos problemas
def func_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        if group == 'admin':
            return redirect('admins')
        if group == 'user':
            return redirect('home')
        if group == 'func':
            return view_func(request, *args, **kwargs)

    return wrapper_func