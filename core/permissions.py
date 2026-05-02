from rest_framework.permissions import BasePermission

class EsJefe(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='jefe').exists()
    
class EsEncargado(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='encargado').exists()

class EsEncargadoOJefe(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        return (
            user.groups.filter(name='encargado').exists() or
            user.groups.filter(name='jefe').exists()
        )
class EsRepresentante(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='representante').exists()
    
class PuedeCrearCliente(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        return (
            user.groups.filter(name='representante').exists() or
            user.groups.filter(name='encargado').exists() or
            user.groups.filter(name='jefe').exists()
        )