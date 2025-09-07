from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm
from django.contrib import messages

from rest_framework import generics, permissions, serializers
from .models import Usuario
from api.serializer import BasicUsuarioSerializer
from .forms import CustomUserCreationForm # Para el registro basado en la API


# Función para verificar si el usuario es administrador
def is_administrador(user):
    return user.is_authenticated and user.rol == 'administrador'


# Función para verificar si el usuario es colaborador o administrador
def is_colaborador_o_administrador(user):
    return user.is_authenticated and (user.rol == 'colaborador' or user.rol == 'administrador')


def registro(request):
    error = None
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        # else:
        #     error = 'Error en el registro. Por favor, revisa los datos.\n'
    else:
        form = CustomUserCreationForm()
    return render(request, 'usuarios/authentication-register.html', {'form': form, 'error': error})


def iniciar_sesion(request):
    context = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
            context = {'error': 'Nombre de usuario o contraseña incorrectos.'}
    return render(request, 'usuarios/authentication-login.html', context=context)


@login_required
def cerrar_sesion(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('iniciar_sesion')


@login_required
def home(request):
    return render(request, 'usuarios/home.html')


@login_required
@user_passes_test(is_administrador)
def vista_admin(request):
    return render(request, 'usuarios/vista_admin.html')


@login_required
@user_passes_test(is_colaborador_o_administrador)
def vista_colaborador(request):
    return render(request, 'usuarios/vista_colaborador.html')


@login_required
def vista_visor(request):
    # Todos los usuarios autenticados pueden ver esta vista
    return render(request, 'usuarios/vista_visor.html')


class UsuarioListCreateAPIView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = BasicUsuarioSerializer
    permission_classes = [permissions.IsAdminUser] # Solo admins pueden listar/crear usuarios vía API

    # Sobrescribir perform_create para usar el formulario de registro y manejar contraseñas
    def perform_create(self, serializer):
        # Crear el usuario usando el CustomUserCreationForm
        # Esto es un poco rudimentario para una API, normalmente usarías un serializador de registro más específico
        # que maneje la contraseña hash automáticamente.
        # Para un registro API limpio, crearías un serializador separado para el registro
        # que no incluya el campo 'rol' o lo maneje de forma predeterminada.

        # Ejemplo simplificado si el serializador tiene la contraseña
        password = self.request.data.get('password')
        if password:
            user = Usuario.objects.create_user(
                username=self.request.data.get('username'),
                email=self.request.data.get('email', ''),
                password=password,
                rol=self.request.data.get('rol', 'visor') # Default a visor si no se especifica
            )
            serializer.instance = user # Asegura que el serializador devuelve la instancia correcta
            messages.success(self.request, 'Usuario creado exitosamente.')
        else:
            messages.error(self.request, 'Se requiere una contraseña para el registro.')
            # Aquí deberías lanzar una excepción o devolver un error de validación HTTP 400
            raise serializers.ValidationError({"password": "Este campo es requerido."})


class UsuarioRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = BasicUsuarioSerializer
    # Solo admins pueden ver/actualizar/eliminar usuarios individuales vía API
    permission_classes = [permissions.IsAdminUser]