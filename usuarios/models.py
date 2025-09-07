from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ROL_CHOICES = (
        ('administrador', 'Administrador'),
        ('colaborador', 'Colaborador'),
        ('visor', 'Visor'),
    )
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='visor')

    # Añade related_name para evitar conflictos con el modelo User de Django
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions '
                  'granted to each of their groups.',
        related_name="app_usuarios_groups", # Nombre único para tu app
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="app_usuarios_user_permissions", # Nombre único para tu app
        related_query_name="usuario",
    )

    def __str__(self):
        return self.username
