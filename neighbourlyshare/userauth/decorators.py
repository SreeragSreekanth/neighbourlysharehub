# userauth/decorators.py

from django.core.exceptions import PermissionDenied

def role_required(allowed_roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                raise PermissionDenied  # Deny access if the role is not allowed
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
