from rest_framework.viewsets import ModelViewSet

from users.permissions import IsTeacher, IsAdmin, IsStudent
from .models import Attendance
from .serializers import AttendanceSerializer
from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger("custom")


class AttendanceViewSet(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsTeacher() or IsAdmin()]
        elif self.action in ["retrieve"]:
            return [IsAuthenticated(), IsStudent() or IsTeacher() or IsAdmin()]
        elif self.action in ["list"]:
            return [IsAuthenticated(), IsTeacher() or IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == "student":
            return Attendance.objects.filter(user=user)
        return super().get_queryset()

    def perform_create(self, serializer):
        attendance = serializer.save()
        logger.info(
            f"Attendance marked: Student {attendance.student.user.username} - "
            f"Course {attendance.course.name} - Status {attendance.status}"
        )
