from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def login_view(request):
    if request.method == 'POST':
        nombre_usu = request.POST.get('nombre_usu')
        password = request.POST.get('password')
        user = authenticate(request, username=nombre_usu, password=password)
        if user is not None:
            if user.estado == '1':  # Solo permite usuarios con estado activo
                login(request, user)
                return redirect('base')  # Redirige si el login es válido
            else:
                messages.error(request, "Tu cuenta está inactiva. Contacta al administrador.")
        else:
            messages.error(request, "Credenciales incorrectas.")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige al login al cerrar sesión


"""def base_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'base.html')"""
    
@login_required
def base_view(request):
    usuario = request.user  # Usuario autenticado
    try:
        empresa = usuario.empresa  # Empresa asociada al usuario
        sucursal = usuario.sucursal  # Sucursal asociada al usuario
    except AttributeError:
        empresa = None
        sucursal = None
    context = {
        'nombre_usuario': usuario.nombre_usu,
        'empresa': empresa,  # Pasamos la empresa
        'sucursal': sucursal,  # Pasamos la sucursal
    }
    
    return render(request, 'base.html', context)

