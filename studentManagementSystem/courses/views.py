from rest_framework.viewsets import ModelViewSet
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from users.permissions import IsTeacher, IsAdmin
from django.core.cache import cache
from rest_framework.decorators import action
from rest_framework.response import Response


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("name",)

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsTeacher() or IsAdmin()]
        return [IsAuthenticated()]

    @action(detail=False, methods=["get"])
    def cached_list(self, request):
        user = request.user
        cache_key = f"courses_list_{user.id}"
        courses = cache.get(cache_key)

        if not courses:
            if user.role == "teacher":
                courses = Course.objects.filter(instructor=user)
            elif user.role == "student":
                courses = Course.objects.filter(enrollment__student__user=user)
            else:
                courses = Course.objects.all()

            cache.set(cache_key, courses, timeout=3600)

        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class EnrollmentViewSet(ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("course_id", "student_id")

    def get_permission(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsTeacher() or IsAdmin()]
        return [IsAuthenticated()]
