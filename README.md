## Prueba Fullstack Django + Framework reactivo
### Objetivo: 
Desarrollar una aplicación web fullstack utilizando Django para el backend y
React o algún otro framework para el frontend. La aplicación debe ser desplegada en un
repositorio de GitHub y, opcionalmente, desplegada en un servidor gratuito.
Tema: Plataforma de Gestión de Proyectos Simplificada

Requisitos Funcionales:
1. Autenticación de Usuarios:
o Los usuarios deben poder registrarse, iniciar sesión y cerrar sesión.
o Implementar roles de usuario (administrador, colaborador, visor) con
diferentes niveles de acceso.

2. Gestión de Proyectos:
o Los usuarios (administradores y colaboradores) deben poder crear, editar y
eliminar proyectos.
o Cada proyecto debe tener un nombre, descripción, fecha de inicio, fecha de
fin y estado (pendiente, en progreso, completado, cancelado).

3. Gestión de Tareas:
o Los usuarios (administradores y colaboradores) deben poder crear, editar y
eliminar tareas dentro de un proyecto.
o Cada tarea debe tener un nombre, descripción, estado (pendiente, en
progreso, completado), asignado a un usuario y fecha de vencimiento.

4. Asignación de Usuarios a Proyectos:
o Los administradores deben poder asignar usuarios (colaboradores y visores)
a proyectos.
5. Comentarios en Tareas:
o Los usuarios asignados a una tarea deben poder agregar comentarios a la
tarea.

6. Notificaciones (Opcional):
o Implementar un sistema básico de notificaciones para eventos importantes
(ej. nueva tarea asignada, tarea completada).

Requisitos Técnicos:
 Backend:
o Django con Django REST Framework para la API.
o Base de datos PostgreSQL (o SQLite para desarrollo).
o Autenticación basada en tokens (ej. JWT).
 Frontend:
o React con un framework de componentes (ej. Material UI, Chakra UI,
Tailwind CSS).
o Gestión de estado con Redux o Context API.
o Routing con React Router.
 Repositorio:

o Código fuente en un repositorio de GitHub.
o Documentación básica del proyecto (README).
 Despliegue (Opcional):
o Despliegue del backend en un servicio gratuito (ej. PythonAnywhere).
o Despliegue del frontend en un servicio gratuito (ej. Netlify, Vercel).

Criterios de Evaluación:
 Funcionalidad: Cumplimiento de los requisitos funcionales.
 Calidad del Código:
o Código limpio, legible y bien comentado.
o Uso de buenas prácticas de programación en Django y React.
o Estructura clara del proyecto.
 Diseño de la Base de Datos:
o Modelo de datos eficiente y bien diseñado.
 API REST:
o API RESTful bien diseñada y documentada.
 Experiencia de Usuario:
o Interfaz de usuario intuitiva y fácil de usar.
 Despliegue (Opcional):
o Configuración y despliegue correctos en los servicios gratuitos.

Entrega:
 Enlace al repositorio de GitHub.
 (Opcional) Enlaces a las versiones desplegadas del backend y frontend.
