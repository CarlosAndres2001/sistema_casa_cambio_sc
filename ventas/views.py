from pyexpat.errors import messages
from django.contrib import messages
from .models import Cliente, CasaCambio,Moneda,Usuario,Sucursal
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from datetime import date
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from django.db.models import Q
from datetime import datetime, timedelta


def clientes(request):
    return render(request, 'ventas/clientes.html')

def ventaa(request):
    return render(request, 'ventas/ventaaa.html')

def pagos(request):
    return render(request, 'ventas/pagos.html')

def registrar_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        nro_documento = request.POST.get('nit')
        telefono = request.POST.get('telefono')
        estado = request.POST.get('estado')

        if Cliente.objects.filter(nro_documento=nro_documento).exists():
            messages.error(request, 'El número de documento registrado pertenece a otro cliente.')
            return render(request, 'ventas/clientes.html')
        
        Cliente.objects.create(
            nombre_cliente=nombre,
            nro_documento=nro_documento,
            telefono=telefono,
            estado=estado
        )

        messages.success(request, 'Cliente registrado correctamente')
        return render(request, 'ventas/clientes.html')

    return render(request, 'ventas/clientes.html')

def lista_clientes(request):
    clientes = Cliente.objects.all() 
    return render(request, 'ventas/listar_clientes.html', {'clientes': clientes})

@login_required
def registrar_venta(request):
    Moneda.objects.all()
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

            nueva_venta = CasaCambio.objects.create(
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

            messages.success(request, 'Venta registrada exitosamente.')
            return redirect('ticket_venta', venta_id=nueva_venta.id_operacion)

        except Exception as e:
            messages.error(request, f'Error al registrar la venta: {str(e)}')
            return redirect('registrar_venta')

    monedas = Moneda.objects.all()
    return render(request, 'ventas/ventaaa.html', {'monedas': monedas})

def ticket_venta(request, venta_id):
    venta = CasaCambio.objects.get(id_operacion=venta_id)
    return render(request, 'ventas/comprobante_venta.html', {'venta': venta})

def ticket_ventaaa(request, venta_id):
    venta = CasaCambio.objects.get(id_operacion=venta_id)
    return render(request, 'ventas/comprobante_ventaa.html', {'venta': venta})
   
@require_POST
def eliminar_venta(request):
    id_venta = request.POST.get('id_venta')
    nota = request.POST.get('nota')
    venta = CasaCambio.objects.get(pk=id_venta)
    venta.nota_anulacion = nota
    venta.estado = '0'  # O False si usas BooleanField
    venta.save()
    messages.success(request, f"La venta #{venta.id_operacion} fue eliminada correctamente.")
    return redirect('lista_ventas')

def lista_ventas(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    moneda_id = request.GET.get('moneda')
    usuario_id = request.GET.get('usuario')  # corregido
    sucursal_id = request.GET.get('sucursal')  # corregido

    ventas = CasaCambio.objects.filter(estado=1)

    if fecha_inicio and fecha_fin:
        fecha_inicio = parse_date(fecha_inicio)
        fecha_fin = parse_date(fecha_fin)
        ventas = ventas.filter(fecha__date__range=(fecha_inicio, fecha_fin))
    else:
        hoy = date.today()
        ventas = ventas.filter(fecha__date=hoy)

    if moneda_id:
        ventas = ventas.filter(id_moneda=moneda_id)

    if usuario_id:
        ventas = ventas.filter(usuario_id=usuario_id)

    if sucursal_id:
        ventas = ventas.filter(sucursal=sucursal_id)

    monedas = Moneda.objects.all()
    usuarios = Usuario.objects.all()
    sucursales = Sucursal.objects.all()

    context = {
        'ventas': ventas,
        'monedas': monedas,
        'usuarios': usuarios,
        'sucursales': sucursales,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'moneda_id': moneda_id,
        'usuario_id': usuario_id,
        'sucursal_id': sucursal_id,
        'today': now().date() 
    }
    return render(request, 'ventas/reporte_ventas.html', context)


