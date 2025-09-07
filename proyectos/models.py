from django.db import models
from django.conf import settings

class Proyecto(models.Model):
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    )

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True) # Puede ser nulo si no hay fecha de fin definida
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    # Relación con el usuario que creó el proyecto
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Si el usuario se elimina, el creador se establece en NULL
        related_name='proyectos_creados',
        null=True, blank=True # Puede ser nulo si el creador es eliminado
    )

    # Opcional: Para asignar colaboradores directamente a un proyecto
    colaboradores = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='proyectos_colaborando',
        blank=True
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['nombre'] # Ordena los proyectos por nombre por defecto

    def __str__(self):
        return self.nombre


class Tarea(models.Model):

    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completado', 'Completado'),
    )

    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE, # Si se elimina el proyecto, también se eliminan sus tareas
        related_name='tareas' # Para acceder a las tareas de un proyecto: proyecto.tareas.all()
    )

    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_vencimiento = models.DateField(blank=True, null=True)

    # Asigna la tarea a un usuario (colaborador o administrador)
    asignado_a = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='tareas_asignadas',
        null=True, blank=True # Puede ser nulo si el usuario asignado es eliminado
    )

    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='tareas_creadas',
        null=True, blank=True
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        ordering = ['proyecto__nombre', 'fecha_vencimiento', 'nombre']

    def __str__(self):
        return f"{self.nombre} ({self.proyecto.nombre})"


class Comentario(models.Model):

    tarea = models.ForeignKey(
        Tarea,
        on_delete=models.CASCADE, # Si se elimina la tarea, sus comentarios también
        related_name='comentarios' # Para acceder a los comentarios de una tarea: tarea.comentarios.all()
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Si el autor es eliminado, el comentario no se borra, el autor se establece en NULL
        related_name='comentarios_escritos',
        null=True, blank=True
    )
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ['fecha_creacion'] # Los comentarios se ordenan por fecha de creación

    def __str__(self):
        return f"Comentario de {self.autor.username if self.autor else 'Anónimo'} en {self.tarea.nombre}"
