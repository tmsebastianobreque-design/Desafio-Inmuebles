from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Inmueble, Usuario, SolicitudArriendo, Comuna, Region
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.views import View
from .forms import RegistroForm
from .forms import InmuebleForm
from django.utils import timezone 
from django.http import JsonResponse



# Create your views here.

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_inmuebles:login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})



def crea_inmueble(datos):
    obj_inmueble = Inmueble(
        nombre=datos['nombre'],
        descripcion=datos['descripcion'],
        m2_construidos=datos['m2_construidos'],
        m2_totales=datos['m2_totales'],
        estacionamientos=datos['estacionamientos'],
        habitaciones=datos['habitaciones'],
        banos=datos['banos'],
        direccion=datos['direccion'],
        comuna_id=datos['comuna_id'],
        tipo_inmueble_id=datos['tipo_inmueble_id'],
        precio_mensual=datos['precio_mensual'],
        propietario_id=datos['id_propietario']
    )
    obj_inmueble.save()
    return obj_inmueble

def listar_inmuebles():
    obj_inmuebles = Inmueble.objects.all() 
    return obj_inmuebles

def actualizar_inmueble(id_inmueble, datos):
    try:
        obj_inmueble = Inmueble.objects.get(id=id_inmueble)
        for key, value in datos.items():
            setattr(obj_inmueble, key, value)
        obj_inmueble.save()
        return True
    except Inmueble.DoesNotExist:
        return False

    
def elimina_inmueble(id_inmueble):
    inmueble = Inmueble.objects.get(id=id_inmueble)
    inmueble.delete()



def crea_usuario(datos):
    user_base = User.objects.create(
        username=datos['rut'],
        first_name=datos['nombres'],
        last_name=datos['apellidos'],
        email=datos['correo_electronico']
         )
    user_base.set_password("password_por_defecto_123")
    user_base.save()

    obj_usuario = Usuario(
        rut=datos['rut'],
        direccion=datos['direccion'],
        telefono=datos['telefono'],
        tipo_usuario=datos['tipo_usuario'],
        user_id=user_base.id  
    )
    obj_usuario.save()
    return obj_usuario


def listar_usuarios():
    obj_usuarios = Usuario.objects.all()
    return obj_usuarios


def actualizar_usuario(id_usuario, datos):
    try:
        obj_usuario = Usuario.objects.get(id=id_usuario)
        
        user_base = obj_usuario.user
        if 'nombres' in datos:
            user_base.first_name = datos['nombres']
        if 'apellidos' in datos:
            user_base.last_name = datos['apellidos']
        if 'correo_electronico' in datos:
            user_base.email = datos['correo_electronico']
        user_base.save()

        for key, value in datos.items():
            if key not in ['nombres', 'apellidos', 'correo_electronico']:
                setattr(obj_usuario, key, value)
                
        obj_usuario.save()
        return True
    except Usuario.DoesNotExist:
        return False


def elimina_usuario(id_usuario):
    try:
        usuario = Usuario.objects.get(id=id_usuario)
        usuario.user.delete()
        return True
    except Usuario.DoesNotExist:
        return False



    

def crea_solicitud_arriendo(datos):
    obj_solicitud = SolicitudArriendo(
        arrendatario_id=datos['id_arrendatario'],  
        inmueble_id=datos['id_inmueble'],          
        estado=datos.get('estado', 'pendiente')   
    )
    obj_solicitud.save()
    return obj_solicitud


def listar_solicitudes_arriendo():
    obj_solicitudes = SolicitudArriendo.objects.all()
    return obj_solicitudes


def actualizar_solicitud_arriendo(id_solicitud, datos):
    try:
        obj_solicitud = SolicitudArriendo.objects.get(id=id_solicitud)
        for key, value in datos.items():
            setattr(obj_solicitud, key, value)
        obj_solicitud.save()
        return True
    except SolicitudArriendo.DoesNotExist:
        return False


def elimina_solicitud_arriendo(id_solicitud):
    try:
        solicitud = SolicitudArriendo.objects.get(id=id_solicitud)
        solicitud.delete()
        return True
    except SolicitudArriendo.DoesNotExist:
        return False



def crea_comuna(cod, nombre, cod_region):
    region = Region.objects.get(cod=cod_region)
    comuna = Comuna(cod=cod, nombre=nombre, region=region)
    comuna.save()
    return comuna

def listar_comunas():
    return Comuna.objects.all()

def actualiza_comuna(cod_comuna, nuevo_nombre):
    comuna = Comuna.objects.get(cod=cod_comuna)
    comuna.nombre = nuevo_nombre
    comuna.save()
    return comuna

def elimina_comuna(cod_comuna):
    comuna = Comuna.objects.get(cod=cod_comuna)
    comuna.delete()



def home(request):
    return render(request, 'home.html')


def sign_out(request):
    logout(request)
    return redirect('/')

def log_in(request):
    if request.method == "GET":
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST["password"])
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'El usuario o contraseña son incorrectos'
            })
        else:
            login(request, user)
            return redirect('/bienvenido')


class RegistroUsuarioView(View):
    """
    Controla el flujo de registro unificado. Crea la cuenta base (User)
    y el perfil extendido (Usuario) con RUT, Dirección y Teléfono de forma simultánea.
    """
    def get(self, request):
        # Al ingresar a la página se genera el formulario vacío
        form = RegistroForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        # Al presionar el botón de envío se procesan los datos ingresados
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save() # Guarda el User y crea automáticamente el Usuario en la base de datos
            return redirect('gestion_inmuebles:login') 
        
        # Si hay errores, vuelve a pintar el formulario mostrando las alertas
        return render(request, 'register.html', {'form': form})



# =====================================================================
# DECORADORES DE SEGURIDAD PERSONALIZADOS
# =====================================================================

def rol_requerido(rol_permitido):
    """
    Decorador personalizado que valida el campo 'tipo_usuario' en la base de datos.
    Si el rol no coincide, bloquea el acceso con un error 403 (Prohibido).
    """
    def decorador(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            try:
                perfil = Usuario.objects.get(user=request.user)
                if perfil.tipo_usuario == rol_permitido:
                    return view_func(request, *args, **kwargs)
            except Usuario.DoesNotExist:
                pass
            raise PermissionDenied  # Lanza un error 403 de Django
        return _wrapped_view
    return decorador


# =====================================================================
# VISTAS DE PERFIL Y PANELES (Basadas en Funciones con Login Requerido)
# =====================================================================

@login_required
def vista_inicio_exitoso(request):
    """
    Página de aterrizaje (Dashboard de bienvenida) tras un login correcto.
    """
    try:
        # Obtenemos el perfil extendido del usuario conectado
        perfil_usuario = Usuario.objects.get(user=request.user)
    except Usuario.DoesNotExist:
        perfil_usuario = None

    return render(request, 'exito.html', {
        'user': request.user,
        'perfil': perfil_usuario
    })


@login_required
def vista_perfil(request):
    """
    Muestra la información de perfil actual del usuario logueado.
    """
    try:
        # Obtenemos la información extendida del usuario conectado
        perfil_usuario = Usuario.objects.get(user=request.user)
    except Usuario.DoesNotExist:
        perfil_usuario = None
        
    return render(request, 'perfil.html', {
        'user': request.user,
        'perfil': perfil_usuario
    })


@login_required
def vista_editar_perfil(request):
    """
    Procesa y actualiza los datos del perfil utilizando la función CRUD del proyecto.
    """
    try:
        perfil_usuario = Usuario.objects.get(user=request.user)
    except Usuario.DoesNotExist:
        return redirect('gestion_inmuebles:perfil')

    if request.method == 'POST':
        # 1. Capturamos los datos enviados por el usuario desde el formulario HTML
        datos_actualizados = {
            'nombres': request.POST.get('first_name'),
            'apellidos': request.POST.get('last_name'),
            'correo_electronico': request.POST.get('email'),
            'direccion': request.POST.get('direccion'),
            'telefono': request.POST.get('telefono'),
        }
        
        # 2. Reutilizamos la función CRUD pasándole el ID correcto
        actualizar_usuario(perfil_usuario.id, datos_actualizados)
        return redirect('gestion_inmuebles:perfil')
        
    return render(request, 'editar_perfil.html', {
        'user': request.user,
        'perfil': perfil_usuario
    })


# =====================================================================
# VISTAS DE ROLES EXCLUSIVOS (Protegidas por Tipo de Usuario)
# =====================================================================

@rol_requerido('arrendador')
def vista_panel_arrendador(request):
    
    mis_inmuebles = Inmueble.objects.filter(propietario=request.user)
    
  
    print(f"--- DEBUG PANEL: El usuario {request.user.username} tiene {mis_inmuebles.count()} propiedades ---")
    
    return render(request, 'panel_arrendador.html', {'mis_inmuebles': mis_inmuebles})



@rol_requerido('arrendatario')
def vista_panel_arrendatario(request):
    """
    Requerimiento 3: Panel exclusivo para usuarios que buscan propiedades.
    Muestra la oferta total disponible en el sistema.
    """
    inmuebles_disponibles = Inmueble.objects.filter(disponible=True)
    return render(request, 'panel_arrendatario.html', {'inmuebles': inmuebles_disponibles})


# =====================================================================
# GESTIÓN DE INMUEBLES - CRUD HITO 4 (Exclusivos para Arrendadores)
# =====================================================================

@rol_requerido('arrendador')
def vista_agregar_inmueble(request):
  
    if request.method == 'POST':
        form = InmuebleForm(request.POST, request.FILES)
        
        if form.is_valid():
            inmueble = form.save(commit=False)
            inmueble.propietario = request.user
            
            if not inmueble.fecha_creacion:
                inmueble.fecha_creacion = timezone.now()
                
            inmueble.save()
            return redirect('gestion_inmuebles:panel_arrendador')
        else:
            print("--- DETECCIÓN DE ERRORES EN FORMULARIO INMUEBLE ---")
            print(form.errors)
            print("-------------------------------------------------")
    else:
        form = InmuebleForm()
        
    return render(request, 'agregar_inmueble.html', {'form': form})



@rol_requerido('arrendador')
def vista_editar_inmueble(request, pk):
    """
    Requerimiento 2a: Permite a los arrendadores actualizar un inmueble existente.
    """
    inmueble = get_object_or_404(Inmueble, pk=pk, propietario=request.user)
    if request.method == 'POST':
        form = InmuebleForm(request.POST, instance=inmueble)
        if form.is_valid():
            form.save()
            return redirect('gestion_inmuebles:panel_arrendador')
    else:
        form = InmuebleForm(instance=inmueble)
        
    return render(request, 'editar_inmueble.html', {'form': form, 'inmueble': inmueble})


@rol_requerido('arrendador')
def vista_borrar_inmueble(request, pk):
    """
    Requerimiento 2b: Permite a los arrendadores eliminar un inmueble existente.
    """
    inmueble = get_object_or_404(Inmueble, pk=pk, propietario=request.user)
    if request.method == 'POST':
        inmueble.delete()
        return redirect('gestion_inmuebles:panel_arrendador')
        
    return render(request, 'borrar_inmueble.html', {'inmueble': inmueble})

def cargar_comunas(request):
    region_id = request.GET.get('region_id')
    comunas = Comuna.objects.filter(region_id=region_id).order_by('nombre')
    return JsonResponse(list(comunas.values('id', 'nombre')), safe=False)