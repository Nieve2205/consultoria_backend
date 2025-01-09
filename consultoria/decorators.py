from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def admin_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({
                'error': 'Acceso denegado. Se requieren privilegios de administrador.'
            }, status=status.HTTP_403_FORBIDDEN)
        return view_func(request, *args, **kwargs)
    return wrapped_view