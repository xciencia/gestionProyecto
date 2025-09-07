from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from .views import ListadoProyecto, ProyectoCreateView, ProyectoUpdateView, ProyectoDeleteView, ProyectoView, \
    TareaCreateView, TareaUpdateView, TareaDeleteView, TareaView, ListadoTarea, ComentarioView, ComentarioCreateView, \
    ComentarioUpdateView, ComentarioDeleteView, ListadoComentario, ListadoAsignacionProyecto, \
    ProyectoAsignacionUpdateView, ProyectoAsignacionView, ListadoRol, RolUpdateView, RolView

urlpatterns = [
    path('listado-proyecto/', login_required(ListadoProyecto.as_view()), name='listado-proyecto'),
    path('crear-proyecto/', login_required(ProyectoCreateView.as_view()), name='crear-proyecto'),
    path('edit-proyecto/<int:pk>/',  login_required(ProyectoUpdateView.as_view()), name='edit-proyecto'),
    path('delete-proyecto/<int:pk>/', login_required(ProyectoDeleteView.as_view()), name='delete-proyecto'),
    path('view-proyecto/<int:pk>/', login_required(ProyectoView.as_view()), name='view-proyecto'),

    path('listado-asignacion-proyecto/', login_required(ListadoAsignacionProyecto.as_view()), name='listado-asignacion-proyecto'),
    path('edit-asignacion-proyecto/<int:pk>/', login_required(ProyectoAsignacionUpdateView.as_view()), name='edit-asignacion-proyecto'),
    path('view-asignacion-proyecto/<int:pk>/', login_required(ProyectoAsignacionView.as_view()), name='view-asignacion-proyecto'),

    path('listado-rol/', login_required(ListadoRol.as_view()), name='listado-rol'),
    path('edit-rol/<int:pk>/', login_required(RolUpdateView.as_view()), name='edit-rol'),
    path('view-rol/<int:pk>/', login_required(RolView.as_view()), name='view-rol'),

    path('listado-tarea/', login_required(ListadoTarea.as_view()), name='listado-tarea'),
    path('crear-tarea/', login_required(TareaCreateView.as_view()), name='crear-tarea'),
    path('edit-tarea/<int:pk>/',  login_required(TareaUpdateView.as_view()), name='edit-tarea'),
    path('delete-tarea/<int:pk>/', login_required(TareaDeleteView.as_view()), name='delete-tarea'),
    path('view-tarea/<int:pk>/', login_required(TareaView.as_view()), name='view-tarea'),

    path('listado-comentario/', login_required(ListadoComentario.as_view()), name='listado-comentario'),
    path('crear-comentario/', login_required(ComentarioCreateView.as_view()), name='crear-comentario'),
    path('edit-comentario/<int:pk>/',  login_required(ComentarioUpdateView.as_view()), name='edit-comentario'),
    path('delete-comentario/<int:pk>/', login_required(ComentarioDeleteView.as_view()), name='delete-comentario'),
    path('view-comentario/<int:pk>/', login_required(ComentarioView.as_view()), name='view-comentario'),
]