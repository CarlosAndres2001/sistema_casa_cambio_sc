from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Persona, Usuario, Rol,Empresa
from django.contrib.auth.hashers import make_password
from django.db import transaction    
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario, Rol, Persona, Sucursal

@login_required
def usuarios(request):    
    return render(request, 'usuarios/usuario.html')

@login_required
def crear_rol(request):
    if request.method == 'POST':
        nombre_rol = request.POST.get('nombre_rol')
        if nombre_rol:
            rol = Rol(nombre_rol=nombre_rol)
            rol.save()
            messages.success(request, "Rol creado exitosamente.")
            return redirect('registrar_usuario') 
        else:
            messages.error(request, "El nombre del rol es obligatorio.")
            return render(request, 'usuarios/usuario.html')
    return render(request, 'usuarios/usuario.html')
   
@login_required
def registrar_usuario(request):
    from usuarios.models import Sucursal
    roles = Rol.objects.all()
    sucursales = Sucursal.objects.all()
    if request.method == 'POST':
        try:
            with transaction.atomic():  
                # Obtener datos del formulario
                nombre = request.POST.get('nombre')
                apellido = request.POST.get('apellido')
                fecha_nac = request.POST.get('fecha_nac')
                cedula_identidad = request.POST.get('cedula_identidad')

                # Crear persona
                persona = Persona.objects.create(
                    nombre=nombre,
                    apellido=apellido,
                    fecha_nac=fecha_nac if fecha_nac else None,
                    cedula_identidad=cedula_identidad
                )

                # Obtener más datos del usuario
                nombre_usu = request.POST.get('nombre_usu')
                contrasena = request.POST.get('contrasena')
                id_rol = request.POST.get('roles') 
                #id_empresa = request.POST['empresa']
                id_sucursal = request.POST['sucursal']
                sucursal = Sucursal.objects.get(id_sucursal=id_sucursal)


                # Validar rol
                if not id_rol:
                    messages.error(request, 'Debe seleccionar un rol.')
                    return redirect('registrar_usuario')

                # Validar contraseña
                if not contrasena:
                    messages.error(request, 'La contraseña es obligatoria.')
                    return redirect('registrar_usuario')

                contrasena_hashed = make_password(contrasena)

                # Validar existencia del rol
                try:
                    rol = Rol.objects.get(id_rol=id_rol)
                except Rol.DoesNotExist:
                    messages.error(request, 'Rol no encontrado.')
                    return redirect('registrar_usuario')
                # Validar si el nombre de usuario ya existe
                if Usuario.objects.filter(nombre_usu=nombre_usu).exists():
                    messages.error(request, 'El nombre de usuario ya existe. Intente con otro.')
                    return redirect('registrar_usuario')

                # Crear usuario
                Usuario.objects.create(
                    nombre_usu=nombre_usu,
                    password=contrasena_hashed,  
                    estado='1',  # Asumiendo que 'estado' es un checkbox o valor booleano
                    rol=rol,
                    persona=persona,
                    empresa = request.user.empresa,
                    sucursal = sucursal
                )

                # Mensaje de éxito
                messages.success(request, 'Usuario registrado exitosamente.')
                return redirect('registrar_usuario')

        except Exception as e:
            messages.error(request, f'Error al registrar usuario: {e}')
            return redirect('registrar_usuario')

    else:
        return render(request, 'usuarios/usuario.html', {'roles': roles, 'sucursales': sucursales})
    

@login_required
def lista_usuarios(request):
    usuarios = Usuario.objects.filter(estado=1).select_related('rol', 'persona', 'sucursal')
    roles = Rol.objects.all()
    personas = Persona.objects.all()
    sucursales = Sucursal.objects.all()

    return render(request, 'usuarios/lista_usuarios.html', {
        'usuarios': usuarios,
        'roles': roles,
        'personas': personas,
        'sucursales': sucursales,  
    })
    
@login_required
@require_POST    
def eliminar_usuario(request):
    id_usuario = request.POST.get('id_usuario')
    usuario = Usuario.objects.get(pk=id_usuario)
    usuario.nombre_usu = request.POST.get('nombre_usu')
    usuario.is_active = 0
    usuario.estado = 0 
    usuario.save()
    messages.success(request, 'Usuario eliminado correctamente')
    return redirect('lista_usuarios')  

@login_required
@require_POST
def editar_usuario(request):
    id_usuario = request.POST.get('id_usuario')
    usuario = Usuario.objects.get(pk=id_usuario)
    
    usuario.nombre_usu = request.POST.get('nombre_usu')
    usuario.rol_id = request.POST.get('rol')
    usuario.sucursal_id = request.POST.get('sucursal')
    usuario.save()
    messages.success(request, 'Usuario modificado con éxito')
    return redirect('lista_usuarios')

@login_required
def editar_empresa(request):
    empresa = get_object_or_404(Empresa, pk=1)  # Suponiendo que solo tienes 1 empresa

    if request.method == 'POST':
        empresa.nombre_empresa = request.POST.get('nombre_empresa')
        empresa.estado = 1
        empresa.direccion = request.POST.get('direccion')
        empresa.telefono = request.POST.get('telefono')
        
        empresa.save()
        messages.success(request, "Información de la empresa actualizada.")
        return redirect('editar_empresa')

    return render(request, 'usuarios/empresa.html', {'empresa': empresa})


@login_required
def crear_sucursal(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_sucursal')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        Sucursal.objects.create(
            nombre_sucursal=nombre,
            direccion=direccion,
            telefono=telefono,
            estado=1  # Valor por defecto (1 = activo)
            
        )
        messages.success(request, "Sucursal creada correctamente.")
        return redirect('crear_sucursal')

    return render(request, 'usuarios/sucursal.html')

@login_required
def lista_sucursal(request):
    sucursales = Sucursal.objects.filter(estado=1)
    return render(request, 'usuarios/lista_sucursal.html', {'sucursales': sucursales})

@login_required
@require_POST
def editar_sucursal(request):
    id_sucursal = request.POST.get('id_sucursal') 
    sucursal = Sucursal.objects.get(pk=id_sucursal)

    if request.method == 'POST':
        sucursal.nombre_sucursal = request.POST.get('nombre_sucursal')
        sucursal.estado = 1
        sucursal.direccion = request.POST.get('direccion')
        sucursal.telefono = request.POST.get('telefono')
        
        sucursal.save()
        messages.success(request, "Información de la sucursal actualizada.")
        return redirect('lista_sucursal')

    return render(request, 'usuarios/lista_sucursal.html')
