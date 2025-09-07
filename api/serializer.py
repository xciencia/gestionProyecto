from rest_framework import serializers
from usuarios.models import Usuario
from proyectos.models import Proyecto, Tarea, Comentario

# from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny


class BasicUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol']


# Serializador para Comentario
class ComentarioSerializer(serializers.ModelSerializer):
    autor = BasicUsuarioSerializer(read_only=True) # Muestra el usuario completo, no solo el ID
    # Si se quiere permitir que se asigne el autor al crear, tendrías que usar:
    # autor = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Comentario
        fields = ['id', 'tarea', 'autor', 'contenido', 'fecha_creacion', 'fecha_actualizacion']
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion', 'autor'] # El autor se asigna en la vista


# Serializador para Tarea
class TareaSerializer(serializers.ModelSerializer):
    asignado_a = BasicUsuarioSerializer(read_only=True) # Muestra el usuario asignado
    creado_por = BasicUsuarioSerializer(read_only=True) # Muestra el usuario creador
    # Si se quiere que se pueda asignar a un usuario por ID al crear/editar:
    # asignado_a_id = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all(), source='asignado_a', write_only=True, required=False, allow_null=True)

    comentarios = ComentarioSerializer(many=True, read_only=True) # Anida los comentarios de la tarea

    class Meta:
        model = Tarea
        fields = [
            'id', 'proyecto', 'nombre', 'descripcion', 'estado',
            'fecha_vencimiento', 'asignado_a', 'creado_por',
            'fecha_creacion', 'fecha_actualizacion', 'comentarios'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion', 'creado_por', 'comentarios']


# Serializador para Proyecto
class ProyectoSerializer(serializers.ModelSerializer):
    creado_por = BasicUsuarioSerializer(read_only=True) # Muestra el usuario creador
    colaboradores = BasicUsuarioSerializer(many=True, read_only=True) # Lista de colaboradores
    # Si se quiere que se puedan asignar colaboradores por ID al crear/editar:
    # colaboradores_ids = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all(), source='colaboradores', write_only=True, many=True, required=False, allow_null=True)

    tareas = TareaSerializer(many=True, read_only=True) # Anida las tareas del proyecto

    class Meta:
        model = Proyecto
        fields = [
            'id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'estado',
            'creado_por', 'colaboradores',
            'fecha_creacion', 'fecha_actualizacion', 'tareas'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion', 'creado_por', 'tareas']

    # Método para manejar el campo de colaboradores al crear/actualizar
    # DRF automáticamente gestiona las relaciones ManyToMany si los IDs están en el campo
    # Pero si se usa `PrimaryKeyRelatedField` con `write_only=True`, necesitarías sobreescribir create/update
    def create(self, validated_data):
        colaboradores_data = validated_data.pop('colaboradores', []) # Extrae los IDs de colaboradores
        proyecto = Proyecto.objects.create(**validated_data)
        proyecto.colaboradores.set(colaboradores_data) # Asigna los colaboradores
        return proyecto

    def update(self, instance, validated_data):
        colaboradores_data = validated_data.pop('colaboradores', None)
        instance = super().update(instance, validated_data)
        if colaboradores_data is not None:
            instance.colaboradores.set(colaboradores_data)
        return instance