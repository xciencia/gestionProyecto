from django import forms
from django.forms import ModelForm

from usuarios.models import Usuario
from .models import Proyecto, Tarea, Comentario


class ProyectoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Proyecto
        fields = '__all__'
        exclude = ['colaboradores']


class AsignacionProyectoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Proyecto
        fields = '__all__'
        exclude = ['estado', 'fecha_fin', 'fecha_inicio', 'fecha_creacion', 'fecha_actualizacion', 'creado_por']


class RolForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Usuario
        fields = '__all__'
        exclude = ['first_name', 'last_name', 'last_login', 'groups', 'date_joined', 'is_active', 'password'
                   ,'is_staff', 'is_superuser', 'user_permissions', 'email']


class TareaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Tarea
        fields = '__all__'
        exclude = ['fecha']


class ComentarioForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Comentario
        fields = '__all__'
        exclude = ['fecha']
