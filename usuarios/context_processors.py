def datos_usuario(request):
    if request.user.is_authenticated:
        usuario = request.user
        return {
            'usuario': usuario,
            'empresa': usuario.empresa,
            'sucursal': usuario.sucursal,
        }
    return {}
