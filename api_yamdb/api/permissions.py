from rest_framework import permissions


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение доступа только для чтения или только для администратора,
    модератора и автора.
    """

    allowed_user_roles = (
        'admin',
        'moderator',
    )

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role in self.allowed_user_roles
            or obj.author == request.user
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение доступа только для чтения или только для администратора.
    """

    allowed_user_roles = ('admin',)

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (
                request.user.role in self.allowed_user_roles
                or request.user.is_superuser
            )
        )


class IsAdmin(permissions.BasePermission):
    """
    Разрешение на редактирование только для администратора.
    """

    allowed_user_roles = ('admin',)

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role in self.allowed_user_roles
            or request.user.is_staff
        )


class AuthorizedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated)


class AdminOrUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.role == 'admin'
            or request.user.is_staff)
        )


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.role == 'admin'
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == 'admin'
            or request.user.is_staff
        )
