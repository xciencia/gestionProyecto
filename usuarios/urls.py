from django.urls import path
from usuarios import views

# Importa las vistas de API
from .views import (
    UsuarioListCreateAPIView,
    UsuarioRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('iniciar-sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('home/', views.home, name='home'),
    path('admin/', views.vista_admin, name='vista_admin'),
    path('colaborador/', views.vista_colaborador, name='vista_colaborador'),
    path('visor/', views.vista_visor, name='vista_visor'),

    # URLs de la API para Usuarios (protegidas por JWT)
    path('api/usuarios/', UsuarioListCreateAPIView.as_view(), name='api_usuario_list_create'),
    path('api/usuarios/<int:pk>/', UsuarioRetrieveUpdateDestroyAPIView.as_view(),
         name='api_usuario_retrieve_update_destroy'),

]



