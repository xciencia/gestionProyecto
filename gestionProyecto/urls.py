"""
URL configuration for gestionProyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView, # Opcional: para verificar la validez de un token sin refrescarlo
)

import usuarios.views
from proyectos.views import badgets

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', usuarios.views.iniciar_sesion),
    path('usuarios/', include('usuarios.urls')),
    path('proyectos/', include('proyectos.urls')),

    path('badgets/', login_required(badgets), name='badgets'),

    # URLs para autenticación JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Opcional

    # Puedes añadir un path para tu API real, por ejemplo:
    # path('api/', include('tu_app_api.urls')),



]


