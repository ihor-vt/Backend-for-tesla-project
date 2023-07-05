from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission

from .models import Service


class ServiceOnlyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        if token:
            try:
                token = token.split(" ")[1]
                service = Service.objects.get(token=token)
                if token == service.token:
                    return (service, None)
            except Service.DoesNotExist:
                pass
        raise AuthenticationFailed("Invalid service token.")

    def authenticate_header(self, request):
        return "Bearer"


class ServiceOnlyAuthorizationSite(BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, Service):
            service_name = request.user.name
            if service_name == "Сайт" and request.method != "GET":
                return False
            return True
        return False
