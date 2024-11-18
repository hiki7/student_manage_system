from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "student"

    def has_object_permission(self, request, view, obj):
        return hasattr(obj, "user") and obj.user == request.user


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "teacher"

    def has_object_permission(self, request, view, obj):
        return request.user.role == "teacher"


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"

    def has_object_permission(self, request, view, obj):
        return request.user.role == "admin"
