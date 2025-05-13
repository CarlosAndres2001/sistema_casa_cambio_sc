from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Proveedor,CasaCambioCompra,Moneda,Sucursal,Usuario
from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from datetime import datetime, timedelta, date
from django.utils import timezone


def crear_proveedor(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        try:
            proveedor = Proveedor.objects.create(
                nombre=nombre,
                direccion=direccion,
                telefono=telefono)
            messages.success(request, 'Proveedor creado con éxito')
            return redirect('crear_proveedor')
        except Exception as e:
            messages.error(request, 'Error al crear el proveedor')
    return render(request, 'compras/proveedor.html')

@login_required
def registrar_compra(request):
    if request.method == 'POST':
        try:
            def to_int(valor):
                try:
                    return int(valor)
                except (ValueError, TypeError):
                    return 0

            fecha = request.POST.get('fecha_hora')
            corte_100 = to_int(request.POST.get('corte_100'))
            corte_50 = to_int(request.POST.get('corte_50'))
            corte_20 = to_int(request.POST.get('corte_20'))
            corte_10 = to_int(request.POST.get('corte_10'))
            corte_5 = to_int(request.POST.get('corte_5'))
            corte_1 = to_int(request.POST.get('corte_1'))
            id_moneda = to_int(request.POST.get('moneda'))
            moneda = Moneda.objects.get(id_moneda=id_moneda)   
            total_calculado = float(request.POST.get('total_calculado', 0))
            observaciones = request.POST.get('obs')
            precio_venta = float(request.POST.get('precio_unitario', 0))
            total_ganado = float(request.POST.get('total_ganado', 0))

            # Usar usuario autenticado y sus relaciones
            usuario = request.user
            empresa = usuario.empresa
            sucursal = usuario.sucursal
            moneda = Moneda.objects.get(id_moneda=id_moneda)

            nueva_compra = CasaCambioCompra.objects.create(
                fecha=fecha,
                corte_100=corte_100,
                corte_50=corte_50,
                corte_20=corte_20,
                corte_10=corte_10,
                corte_5=corte_5,
                corte_1=corte_1,
                usuario=usuario,
                total_calculado=total_calculado,
                id_moneda=moneda,
                estado=1,
                observaciones=observaciones,
                precio_venta=precio_venta,
                empresa=empresa,
                sucursal=sucursal,
                total_ganado=total_ganado,
                nota_anulacion = ''
            )

            messages.success(request, 'Compra registrada exitosamente.')
            return redirect('ticket_compra', compra_id=nueva_compra.id_operacion_compra)

        except Exception as e:
            messages.error(request, f'Error al registrar la compra: {str(e)}')
            return redirect('registrar_compra')

    monedas = Moneda.objects.all()
    return render(request, 'compras/compra_casa.html', {'monedas': monedas})

@login_required
def ticket_compra(request, compra_id):
    compra = CasaCambioCompra.objects.get(id_operacion_compra=compra_id)
    return render(request, 'compras/comprobante_compra.html', {'compra': compra})

@login_required
def ticket_compraa(request, compra_id):
    compra = CasaCambioCompra.objects.get(id_operacion_compra=compra_id)
    return render(request, 'compras/comprobante_comprap.html', {'compra': compra})

@require_POST
def eliminar_compra(request):
    id_compra = request.POST.get('id_compra')
    nota = request.POST.get('nota')
    compra = CasaCambioCompra.objects.get(pk=id_compra)
    compra.nota_anulacion = nota
    compra.estado = '0'  # O False si usas BooleanField
    compra.save()
    messages.success(request, f"La Compra #{compra.id_operacion_compra} fue eliminada correctamente.")
    return redirect('lista_compra')

@login_required
def lista_compra(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    moneda_id = request.GET.get('moneda')
    usuario_id = request.GET.get('usuario')
    sucursal_id = request.GET.get('sucursal')
    
    compras = CasaCambioCompra.objects.filter(estado=1)
    #compras = CasaCambioCompra.objects.all()
    
    # Filtrar por fechas
    if fecha_inicio and fecha_fin:
        fecha_inicio = parse_date(fecha_inicio)
        fecha_fin = parse_date(fecha_fin)
        compras = compras.filter(fecha__date__range=(fecha_inicio, fecha_fin))
    else:
        hoy = date.today()
        compras = compras.filter(fecha__date=hoy)

    # Filtrar por moneda
    if moneda_id:
        compras = compras.filter(id_moneda=moneda_id)

    # Filtrar por usuario
    if usuario_id:
        compras = compras.filter(usuario_id=usuario_id)

    # Filtrar por sucursal
    if sucursal_id:
        compras = compras.filter(sucursal=sucursal_id)

    context = {
        'compras': compras,
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

    return render(request, 'compras/reporte_compras.html', context)

