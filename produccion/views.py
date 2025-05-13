from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Traspaso, Egreso, Moneda,Categoria, Subcategoria, Usuario,Sucursal
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from usuarios.models import Usuario
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from datetime import date

def gestionar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'produccion/categorias.html', {'categorias': categorias})

def crear_categoria(request):
    if request.method == 'POST':
        nombre_categoria = request.POST.get('nombre_categoria')
        if nombre_categoria:
            if Categoria.objects.filter(nombre_categoria=nombre_categoria).exists():
                messages.error(request, 'La categoría ya existe.')
            else:
                Categoria.objects.create(nombre_categoria=nombre_categoria)
                messages.success(request, 'Categoría creada exitosamente.')
        else:
            messages.error(request, 'El nombre de la categoría no puede estar vacío.')
        return redirect('gestionar_categorias')

def crear_subcategoria(request):
    if request.method == 'POST':
        nombre_subcategoria = request.POST.get('nombre_subcategoria')
        id_categoria = request.POST.get('id_categoria')

        if nombre_subcategoria and id_categoria:
            try:
                categoria = Categoria.objects.get(id_categoria=id_categoria)
                if Subcategoria.objects.filter(nombre_subcategoria=nombre_subcategoria, id_categoria=categoria).exists():
                    messages.error(request, 'La subcategoría ya existe en esta categoría.')
                else:
                    Subcategoria.objects.create(nombre_subcategoria=nombre_subcategoria, id_categoria=categoria)
                    messages.success(request, 'Subcategoría creada exitosamente.')
            except Categoria.DoesNotExist:
                messages.error(request, 'La categoría seleccionada no existe.')
        else:
            messages.error(request, 'Debe completar todos los campos para crear una subcategoría.')
        return redirect('gestionar_categorias')

def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'produccion/lista_categorias.html', {'categorias': categorias})

@login_required
def registrar_traspaso(request):
    from usuarios.models import Sucursal
    if request.method == 'POST':
        fecha_hora = request.POST.get('fecha_hora')
        observaciones = request.POST.get('observaciones')
        monto = request.POST.get('monto')
        id_moneda = request.POST.get('moneda')
        sucursal_destino_id = request.POST.get('sucursal_destino')

        usuario = request.user
        sucursal_origen = usuario.sucursal  # esta es la sucursal del usuario

        try:
            moneda = Moneda.objects.get(id_moneda=id_moneda)
            sucursal_destino = Sucursal.objects.get(id_sucursal=sucursal_destino_id)
        except (Moneda.DoesNotExist, Sucursal.DoesNotExist):
            messages.error(request, 'Moneda o Sucursal destino no válida.')
            return redirect('registrar_traspaso')

        Traspaso.objects.create(
            fecha_hora=fecha_hora,
            observaciones=observaciones,
            monto=monto,
            moneda=moneda,
            usuario=usuario,
            sucursal_destino=sucursal_destino,
            estado=1,
            sucursal_origen=sucursal_origen,
            nota_anulacion = ''
        )
        messages.success(request, 'Traspaso creado exitosamente.')
        return redirect('registrar_traspaso')

    sucursales = Sucursal.objects.all()
    monedas = Moneda.objects.all()
    return render(request, 'produccion/traspasos.html', {'monedas': monedas, 'sucursales': sucursales})

@login_required
def registrar_egreso(request):
    if request.method == 'POST':
        fecha_hora = request.POST.get('fecha_hora')
        observaciones = request.POST.get('observaciones')
        monto = request.POST.get('monto')
        id_moneda = request.POST.get('moneda')
        usuario = request.user
        sucursal = usuario.sucursal

        try:
            moneda = Moneda.objects.get(id_moneda=id_moneda)
        except Moneda.DoesNotExist:
            moneda = None

        if moneda:
            Egreso.objects.create(
                fecha_hora=fecha_hora,
                observaciones=observaciones,
                monto=monto,
                moneda=moneda,
                usuario=request.user,
                estado=1,
                sucursal_id = sucursal.id_sucursal,
                nota_anulacion = ''
            )
            messages.success(request, 'Egreso creada exitosamente.')
            return redirect('registrar_egreso')
        else:
            messages.error(request, 'Error al registrar.')

    monedas = Moneda.objects.all()
    return render(request, 'produccion/egresos.html', {'monedas': monedas})

@login_required
def reporte_egresos(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    moneda_id = request.GET.get('moneda')
    usuario_id = request.GET.get('usuario')
    sucursal_id = request.GET.get('sucursal')

    egresos = Egreso.objects.filter(estado=1)

    # Filtrar por fechas
    if fecha_inicio and fecha_fin:
        fecha_inicio = parse_date(fecha_inicio)
        fecha_fin = parse_date(fecha_fin)
        egresos = egresos.filter(fecha_hora__date__range=(fecha_inicio, fecha_fin))
    else:
        hoy = date.today()
        egresos = egresos.filter(fecha_hora__date=hoy)

    # Filtrar por moneda
    if moneda_id :
        egresos = egresos.filter(moneda_id=moneda_id)

    # Filtrar por usuario
    if usuario_id:
        egresos = egresos.filter(usuario_id=usuario_id)

    if sucursal_id:
        egresos = egresos.filter(sucursal=sucursal_id)

    context = {
        'egresos': egresos,
        'sucursales': Sucursal.objects.all(),
        'usuarios': Usuario.objects.all(),
        'monedas': Moneda.objects.all(),
        'fecha_inicio': request.GET.get('fecha_inicio', ''),
        'fecha_fin': request.GET.get('fecha_fin', ''),
        'moneda_id': moneda_id or '',
        'usuario_id': usuario_id or '',
        'sucursal_id': sucursal_id or '',
        'today': timezone.now().date(),
    }
    return render(request, 'produccion/reporte_egresos.html', context)

@login_required
def reporte_traspasos(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    moneda_id = request.GET.get('moneda')
    usuario_id = request.GET.get('usuario')
    sucursal_id = request.GET.get('sucursal')

    traspasos = Traspaso.objects.filter(estado=1)

    # Filtrar por fechas
    if fecha_inicio and fecha_fin:
        fecha_inicio = parse_date(fecha_inicio)
        fecha_fin = parse_date(fecha_fin)
        traspasos = traspasos.filter(fecha_hora__date__range=(fecha_inicio, fecha_fin))
    else:
        hoy = date.today()
        traspasos = traspasos.filter(fecha_hora__date=hoy)

    # Filtrar por moneda
    if moneda_id and moneda_id != 'todos':
        traspasos = traspasos.filter(moneda_id=moneda_id)

    # Filtrar por usuario
    if usuario_id and usuario_id != 'todos':
        traspasos = traspasos.filter(usuario_id=usuario_id)
        
    if sucursal_id:
        traspasos = traspasos.filter(sucursal_destino_id =sucursal_id)

    context = {
        'traspasos': traspasos,
        'monedas': Moneda.objects.all(),
        'usuarios': Usuario.objects.all(),
        'sucursales': Sucursal.objects.all(),
        'fecha_inicio': request.GET.get('fecha_inicio', ''),
        'fecha_fin': request.GET.get('fecha_fin', ''),
        'moneda_id': moneda_id or '',
        'usuario_id': usuario_id or '',
        'sucursal_id': sucursal_id or '',
        'today': timezone.now().date(),
    }
    return render(request, 'produccion/reporte_traspasos.html', context)

@require_POST
def eliminar_traspaso(request):
    id_traspaso = request.POST.get('id_traspaso')
    nota = request.POST.get('nota')
    traspaso = Traspaso.objects.get(pk=id_traspaso)
    traspaso.nota_anulacion = nota
    traspaso.estado = 0  # O False si usas BooleanField
    traspaso.save()
    messages.success(request, f"El traspaso #{traspaso.id_traspaso} fue eliminado correctamente.")
    return redirect('reporte_traspasos')

@require_POST
def eliminar_egreso(request):
    id_egreso = request.POST.get('id_egreso')
    nota = request.POST.get('nota')
    egreso = Egreso.objects.get(pk=id_egreso)
    egreso.nota_anulacion = nota
    egreso.estado = 0  # O False si usas BooleanField
    egreso.save()
    messages.success(request, f"El egreso #{egreso.id_egreso} fue eliminado correctamente.")
    return redirect('reporte_egresos')


