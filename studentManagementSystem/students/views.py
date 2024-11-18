from rest_framework.viewsets import ModelViewSet

from users.permissions import IsStudent, IsAdmin
from .models import Student
from .serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["dob", "registration_date"]

    def get_permission(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated(), IsStudent() or IsAdmin()]
        elif self.action in ["update", "partial_update"]:
            return [IsAuthenticated(), IsStudent()]
        elif self.action in ["destroy"]:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == "student":
            return Student.objects.filter(user=user)
        return Student.objects.all()
