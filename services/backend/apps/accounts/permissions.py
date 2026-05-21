from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Admin yoki Manager - ikkalasi ham to'liq huquqga ega"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ("admin", "manager")


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "teacher"


class IsTutor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "tutor"


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"


class IsParent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "parent"


class IsKomendant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "komendant"


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "manager"


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ("tutor", "komendant", "manager")


class IsAdminOrStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ("admin", "tutor", "komendant", "manager")


class IsEvaluatorOrAdmin(BasePermission):
    """Teacher, tutor, komendant can submit records; admin/manager can also submit."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in (
            "admin", "manager", "teacher", "tutor", "komendant",
        )


class IsAdminOrTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ("admin", "teacher")


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role in ("admin", "manager")


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role in ("admin", "manager"):
            return True
        if hasattr(obj, "user"):
            return obj.user == request.user
        if hasattr(obj, "student"):
            return obj.student.user == request.user
        return False
