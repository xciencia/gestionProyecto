from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rest_framework import generics, permissions

from api.serializer import ProyectoSerializer, TareaSerializer, ComentarioSerializer
from usuarios.models import Usuario
from .models import Proyecto, Tarea, Comentario
from .forms import ProyectoForm, TareaForm, ComentarioForm, AsignacionProyectoForm, RolForm


def badgets(request):
    proyectos = Proyecto.objects.all().count()
    tareas = Tarea.objects.all().count()
    comentarios = Comentario.objects.all().count()
    data = {'proyectos': proyectos, 'tareas': tareas, 'comentarios': comentarios}
    return JsonResponse(data, safe=False)

# Funciones de ayuda para verificar roles (asumiendo que están en usuarios/views.py o un utils.py)
# Si están en usuarios/views.py, deberías importarlas de ahí:
# from usuarios.views import is_administrador, is_colaborador_o_administrador

# Por simplicidad, las replicamos aquí si no quieres importarlas:
def is_administrador(user):
    return user.is_authenticated and user.rol == 'administrador'

def is_colaborador_o_administrador(user):
    return user.is_authenticated and (user.rol == 'colaborador' or user.rol == 'administrador')

@login_required
def lista_proyectos(request):
    proyectos = Proyecto.objects.all().order_by('-fecha_creacion')
    # Opcional: Filtrar proyectos según el usuario logueado o su rol
    # if request.user.rol == 'colaborador':
    #     proyectos = proyectos.filter(Q(creado_por=request.user) | Q(colaboradores=request.user)).distinct()
    # if request.user.rol == 'visor':
    #     proyectos = proyectos.filter(...) # Define qué proyectos puede ver un visor
    return render(request, 'proyectos/lista_proyectos.html', {'proyectos': proyectos})

@login_required
@user_passes_test(is_colaborador_o_administrador)
def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.creado_por = request.user # Asigna el usuario logueado como creador
            proyecto.save()
            form.save_m2m() # Guarda las relaciones ManyToMany como los colaboradores
            messages.success(request, 'Proyecto creado exitosamente.')
            return redirect('detalle_proyecto', pk=proyecto.pk)
        else:
            messages.error(request, 'Error al crear el proyecto. Por favor, revisa los datos.')
    else:
        form = ProyectoForm()
    return render(request, 'proyectos/crear_editar_proyecto.html', {'form': form, 'titulo': 'Crear Proyecto'})

@login_required
def detalle_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    # Aquí puedes añadir lógica para permitir o denegar el acceso a la vista
    # según el rol del usuario o si es colaborador del proyecto.
    # Por ahora, cualquier usuario logueado puede ver los detalles.
    return render(request, 'proyectos/detalle_proyecto.html', {'proyecto': proyecto})

@login_required
@user_passes_test(is_colaborador_o_administrador)
def editar_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)

    # Opcional: Solo el creador o un administrador pueden editar
    if not is_administrador(request.user) and proyecto.creado_por != request.user:
        messages.error(request, 'No tienes permiso para editar este proyecto.')
        return redirect('detalle_proyecto', pk=proyecto.pk)

    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proyecto actualizado exitosamente.')
            return redirect('detalle_proyecto', pk=proyecto.pk)
        else:
            messages.error(request, 'Error al actualizar el proyecto. Por favor, revisa los datos.')
    else:
        form = ProyectoForm(instance=proyecto)
    return render(request, 'proyectos/crear_editar_proyecto.html', {'form': form, 'titulo': 'Editar Proyecto', 'proyecto': proyecto})

@login_required
@user_passes_test(is_administrador) # Solo administradores pueden eliminar proyectos
def eliminar_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        proyecto.delete()
        messages.success(request, 'Proyecto eliminado exitosamente.')
        return redirect('lista_proyectos')
    return render(request, 'proyectos/confirmar_eliminar.html', {'proyecto': proyecto})



# Vista basada en CLASES para listar y crear proyectos, tareas, comentarios
class ProyectoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    # Define permisos, ej: IsAuthenticated para todos, is_colaborador_o_administrador para crear
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Asigna el usuario que crea el proyecto
        serializer.save(creado_por=self.request.user)


# Vista para detalle, actualización y eliminación de proyectos
class ProyectoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    # Define permisos, ej: IsAdminUser o custom permission para creador/colaborador
    permission_classes = [permissions.IsAuthenticated]


class TareaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
    # Define permisos, ej: IsAuthenticated para todos, is_colaborador_o_administrador para crear
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Asigna el usuario que crea el tarea
        serializer.save(creado_por=self.request.user)


class TareaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
    # Define permisos, ej: IsAdminUser o custom permission para creador/colaborador
    permission_classes = [permissions.IsAuthenticated]


class ComentarioListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    # Define permisos, ej: IsAuthenticated para todos, is_colaborador_o_administrador para crear
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Asigna el usuario que crea el tarea
        serializer.save(creado_por=self.request.user)


class ComentarioRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    # Define permisos, ej: IsAdminUser o custom permission para creador/colaborador
    permission_classes = [permissions.IsAuthenticated]


#---------------------------------------------------
# Django -  Modelo Vista Template Basado en CLASE
#---------------------------------------------------
class ListadoProyecto(ListView):
    model = Proyecto
    template_name = 'proyectos/listado.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = list(Proyecto.objects.all().values('id', 'nombre', 'estado'))
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Proyecto'
        context['regresar'] = 'listado-proyecto'
        context['obj'] = [('id', 'Id'), ('nombre', 'nombre'), ('estado', 'estado')]
        context['link'] = ['crear-proyecto', 'listado-proyecto', 'edit-proyecto', 'delete-proyecto', 'view-proyecto']
        return context

    def get_queryset(self):
        return Proyecto.objects.all()


class ProyectoCreateView(CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyectos/CreateView.html'
    success_url = reverse_lazy('listado-proyecto')

    def post(self, request, *args, **kwargs):
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Proyecto'
        context['regresar'] = self.success_url
        context['action'] = 'add'
        return context


class ProyectoUpdateView(UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyectos/CreateView.html'
    success_url = reverse_lazy('listado-proyecto')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        form = ProyectoForm(request.POST)

        if action == 'edit':
            form = self.get_form()
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(self.success_url)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de Proyecto'
        context['regresar'] = self.success_url
        context['action'] = 'edit'
        return context


class ProyectoDeleteView(DeleteView):
    model = Proyecto
    success_url = reverse_lazy('listado-proyecto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Proyecto'
        context['regresar'] = self.success_url
        context['action'] = 'delete'
        return context

    def form_valid(self, form):
        return super(self.__class__, self).form_valid(form)

    def form_invalid(self, form, **kwargs):
        data = {'msg': 'Referencia cruzada'}
        return JsonResponse(data, safe=False)


class ProyectoView(UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyectos/CreateView.html'
    success_url = reverse_lazy('listado-proyecto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Consulta de Proyecto'
        context['regresar'] = self.success_url
        context['action'] = 'view'
        return context


class ListadoAsignacionProyecto(ListView):
    model = Proyecto
    template_name = 'proyectos/listado.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = list(Proyecto.objects.all().values('id', 'nombre', 'estado'))
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Asignacion de Proyecto'
        context['regresar'] = 'listado-asignacion-proyecto'
        context['obj'] = [('id', 'Id'), ('nombre', 'nombre'), ('estado', 'estado')]
        context['link'] = ['', 'listado-asignacion-proyecto',
                           'edit-asignacion-proyecto', '', 'view-asignacion-proyecto']
        return context

    def get_queryset(self):
        return Proyecto.objects.all()


class ProyectoAsignacionUpdateView(UpdateView):
    model = Proyecto
    form_class = AsignacionProyectoForm
    template_name = 'proyectos/CreateView.html'
    success_url = reverse_lazy('listado-asignacion-proyecto')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        form = ProyectoForm(request.POST)

        if action == 'edit':
            form = self.get_form()
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(self.success_url)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de Asignacion de Proyecto'
        context['regresar'] = self.success_url
        context['action'] = 'edit'
        return context


class ProyectoAsignacionView(UpdateView):
    model = Proyecto
    form_class = AsignacionProyectoForm
    template_name = 'proyectos/CreateView.html'
    success_url = reverse_lazy('listado-asignacion-proyecto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Consulta de Asignacion de Proyecto'
        context['regresar'] = self.success_url
        context['action'] = 'view'
        return context


class ListadoRol(ListView):
    model = Usuario
    template_name = 'proyectos/listado.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = list(Usuario.objects.all().values('id', 'username', 'email'))
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Roles de Usuarios'
        context['regresar'] = 'listado-rol'
        context['obj'] = [('id', 'Id'), ('username', 'username'), ('email', 'email')]
        context['link'] = ['', 'listado-rol', 'edit-rol', '', 'view-rol']
        return context

    def get_queryset(self):
        return Usuario.objects.all()


class RolUpdateView(UpdateView):
    model = Usuario
    form_class = RolForm
    template_name = 'proyectos/CreateView.html'
    success_url = reverse_lazy('listado-rol')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        form = ProyectoForm(request.POST)

        if action == 'edit':
            form = self.get_form()
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(self.success_url)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de Rol de Usuarios'
        context['regresar'] = self.success_url
        context['action'] = 'edit'
        return context


class RolView(UpdateView):
    model = Usuario
    form_class = RolForm
    template_name = 'proyectos/CreateView.html'
    success_url = reverse_lazy('listado-rol')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Consulta de Rol de Usuarios'
        context['regresar'] = self.success_url
        context['action'] = 'view'
        return context


class ListadoTarea(ListView):
    model = Tarea
    template_name = 'proyectos/listado.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = list(Tarea.objects.all().values('id', 'proyecto__nombre', 'estado'))
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Tarea'
        context['regresar'] = 'listado-tarea'
        context['obj'] = [('id', 'Id'), ('proyecto__nombre', 'proyecto'), ('estado', 'estado')]
        context['link'] = ['crear-tarea', 'listado-tarea', 'edit-tarea', 'delete-tarea', 'view-tarea']
        return context

    def get_queryset(self):
        return Tarea.objects.all()


class TareaCreateView(CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'proyectos/CreateView.html'
    success_url = reverse_lazy('listado-tarea')

    def post(self, request, *args, **kwargs):
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Tarea'
        context['regresar'] = self.success_url
        context['action'] = 'add'
        return context


class TareaUpdateView(UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'proyectos/CreateView.html'
    success_url = reverse_lazy('listado-tarea')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        form = TareaForm(request.POST)

        if action == 'edit':
            form = self.get_form()
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(self.success_url)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de Tarea'
        context['regresar'] = self.success_url
        context['action'] = 'edit'
        return context


class TareaDeleteView(DeleteView):
    model = Tarea
    success_url = reverse_lazy('listado-tarea')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Tarea'
        context['regresar'] = self.success_url
        context['action'] = 'delete'
        return context

    def form_valid(self, form):
        return super(self.__class__, self).form_valid(form)

    def form_invalid(self, form, **kwargs):
        data = {'msg': 'Referencia cruzada'}
        return JsonResponse(data, safe=False)


class TareaView(UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'proyectos/CreateView.html'
    success_url = reverse_lazy('listado-tarea')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Consulta de Tarea'
        context['regresar'] = self.success_url
        context['action'] = 'view'
        return context


class ListadoComentario(ListView):
    model = Comentario
    template_name = 'proyectos/listado.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = list(Comentario.objects.all().values('id', 'tarea__nombre', 'autor__username'))
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Comentario'
        context['regresar'] = 'listado-comentario'
        context['obj'] = [('id', 'Id'), ('tarea__nombre', 'tarea'), ('autor__username', 'autor')]
        context['link'] = ['crear-comentario', 'listado-comentario', 'edit-comentario', 'delete-comentario',
                           'view-comentario']
        return context

    def get_queryset(self):
        return Comentario.objects.all()


class ComentarioCreateView(CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'proyectos/CreateView.html'
    success_url = reverse_lazy('listado-comentario')

    def post(self, request, *args, **kwargs):
        form = ComentarioForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Comentario'
        context['regresar'] = self.success_url
        context['action'] = 'add'
        return context


class ComentarioUpdateView(UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'proyectos/CreateView.html'
    success_url = reverse_lazy('listado-comentario')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        form = ComentarioForm(request.POST)

        if action == 'edit':
            form = self.get_form()
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(self.success_url)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de Comentario'
        context['regresar'] = self.success_url
        context['action'] = 'edit'
        return context


class ComentarioDeleteView(DeleteView):
    model = Comentario
    success_url = reverse_lazy('listado-comentario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Comentario'
        context['regresar'] = self.success_url
        context['action'] = 'delete'
        return context

    def form_valid(self, form):
        return super(self.__class__, self).form_valid(form)

    def form_invalid(self, form, **kwargs):
        data = {'msg': 'Referencia cruzada'}
        return JsonResponse(data, safe=False)


class ComentarioView(UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'proyectos/CreateView.html'
    success_url = reverse_lazy('listado-comentario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Consulta de Comentario'
        context['regresar'] = self.success_url
        context['action'] = 'view'
        return context

