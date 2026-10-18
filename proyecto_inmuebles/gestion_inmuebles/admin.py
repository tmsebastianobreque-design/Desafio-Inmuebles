from django.contrib import admin
from .models import Inmueble, Region, Comuna, TipoInmueble, Usuario, SolicitudArriendo

# admin.site.register(Region)
# admin.site.register(Comuna)
# admin.site.register(TipoInmueble)
# admin.site.register(Inmueble)
# admin.site.register(Usuario)
# admin.site.register(SolicitudArriendo)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'region')
    search_fields = ('nombre',)
    list_filter = ('region',)


@admin.register(TipoInmueble)
class TipoInmuebleAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'rut', 'telefono', 'tipo_usuario', 'direccion')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'rut')
    list_filter = ('tipo_usuario',)


@admin.register(Inmueble)
class InmuebleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'propietario', 'tipo_inmueble', 'comuna', 'precio_mensual')
    search_fields = ('nombre', 'direccion', 'propietario__username')
    list_filter = ('tipo_inmueble', 'comuna__region', 'comuna')
    list_editable = ('precio_mensual',)


@admin.register(SolicitudArriendo)
class SolicitudArriendoAdmin(admin.ModelAdmin):
    list_display = ('id', 'inmueble', 'arrendatario', 'estado', 'fecha_solicitud')
    list_display_links = ('id', 'inmueble')
    search_fields = ('inmueble__nombre', 'arrendatario__user__username')
    list_filter = ('estado', 'fecha_solicitud')
    list_editable = ('estado',)