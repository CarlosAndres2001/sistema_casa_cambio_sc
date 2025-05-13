from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)  # AutoIncremental
    nombre_rol = models.CharField(max_length=50)

    class Meta:
        db_table = 'rol'

    def __str__(self):
        return self.nombre_rol
class Empresa(models.Model):
    id_empresa = models.AutoField(primary_key=True)  # AutoIncremental
    nombre_empresa = models.CharField(max_length=100)
    direccion = models.CharField(max_length=500)
    telefono = models.CharField(max_length=15)
    estado =models.IntegerField()
    
    class Meta:
        db_table = 'empresa'
        
class Sucursal(models.Model):
    id_sucursal = models.AutoField(primary_key=True)  # AutoIncremental
    nombre_sucursal = models.CharField(max_length=100)
    direccion = models.CharField(max_length=500)
    telefono = models.CharField(max_length=15)
    estado =models.IntegerField()
    
    class Meta:
        db_table = 'sucursal'
        
class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True)  # AutoIncremental
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nac = models.DateField(blank=True, null=True)
    cedula_identidad = models.CharField(unique=True, max_length=20)

    class Meta:
        db_table = 'persona'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    
class Moneda(models.Model):
    id_moneda = models.AutoField(primary_key=True)
    nombre_moneda = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)
    class Meta:
        db_table = 'moneda'

class UsuarioManager(BaseUserManager):
    def create_user(self, nombre_usu, password=None, **extra_fields):
        if not nombre_usu:
            raise ValueError('El nombre de usuario es obligatorio')
        user = self.model(nombre_usu=nombre_usu, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nombre_usu, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('estado', 'activo')
        return self.create_user(nombre_usu, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)
    nombre_usu = models.CharField(max_length=50, unique=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    estado = models.CharField(max_length=30, blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)  
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, null=True, blank=True)


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'nombre_usu'
    REQUIRED_FIELDS = ['rol', 'persona']

    objects = UsuarioManager()

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.nombre_usu
