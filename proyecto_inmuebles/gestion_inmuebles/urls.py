from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'gestion_inmuebles'

urlpatterns = [
    path('', views.home, name='home'),
    
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        next_page='gestion_inmuebles:inicio_exitoso'
    ), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(
        template_name='logout.html',
        next_page='gestion_inmuebles:home'
    ), name='logout'),
    
    path('registro/', views.RegistroUsuarioView.as_view(), name='registro'),
    path('perfil/', views.vista_perfil, name='perfil'),
    path('perfil/editar/', views.vista_editar_perfil, name='editar_perfil'),
    path('bienvenido/', views.vista_inicio_exitoso, name='inicio_exitoso'),
    

    path('arrendador/', views.vista_panel_arrendador, name='panel_arrendador'),
    path('arrendatario/', views.vista_panel_arrendatario, name='panel_arrendatario'),
    path('inmueble/agregar/', views.vista_agregar_inmueble, name='agregar_inmueble'),


    path('inmueble/agregar/', views.vista_agregar_inmueble, name='agregar_inmueble'),
    path('inmueble/editar/<int:pk>/', views.vista_editar_inmueble, name='editar_inmueble'),
    path('inmueble/borrar/<int:pk>/', views.vista_borrar_inmueble, name='borrar_inmueble'),
]
