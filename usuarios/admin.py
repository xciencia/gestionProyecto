from django.contrib import admin
from django.apps import apps

modelos = apps.get_app_config('usuarios').get_models()
for modelo in modelos:
    try:
        admin.site.register(modelo)
    except admin.sites.AlreadyRegistered:
        pass
