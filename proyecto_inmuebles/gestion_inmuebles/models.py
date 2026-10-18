from django.db import models
from django.contrib.auth.models import User



class Region(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Región")

    def __str__(self):
        return self.nombre


class Comuna(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Comuna")
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='comunas',
        verbose_name="Región"
    )


    def __str__(self):
        return self.nombre


class TipoInmueble(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Tipo de Inmueble")

    
    def __str__(self):
        return self.nombre
    

class Inmueble(models.Model):
    propietario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='inmuebles',
        verbose_name="Propietario (Arrendador)"
    )
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    m2_construidos = models.FloatField()
    m2_totales = models.FloatField()
    estacionamientos = models.IntegerField()
    habitaciones = models.IntegerField()
    banos = models.IntegerField()
    direccion = models.CharField(max_length=200)
    comuna = models.ForeignKey(
        Comuna, 
        on_delete=models.CASCADE, 
        related_name='inmuebles',
        verbose_name="Comuna"
    )
    tipo_inmueble = models.ForeignKey(
        TipoInmueble, 
        on_delete=models.PROTECT, 
        related_name='inmuebles',
        verbose_name="Tipo de Inmueble"
    )
    precio_mensual = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(null=True, blank=True)
    disponible = models.BooleanField(default=True)

    
    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('arrendatario', 'Arrendatario'),
        ('arrendador', 'Arrendador'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono Personal")
    tipo_usuario = models.CharField(
        max_length=20, 
        choices=TIPO_USUARIO_CHOICES, 
        default='arrendatario',
        verbose_name="Tipo de Usuario"
    )


class SolicitudArriendo(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]

    arrendatario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='solicitudes',
        verbose_name="Arrendatario Postulante"
    )
    
    inmueble = models.ForeignKey(
        Inmueble, 
        on_delete=models.CASCADE, 
        related_name='solicitudes',
        verbose_name="Inmueble Solicitado"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name="Estado de la Solicitud"
    )
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Solicitud")

    def __str__(self):
       return f"Solicitud de {self.arrendatario.user.username} para {self.inmueble.nombre} ({self.estado})"

