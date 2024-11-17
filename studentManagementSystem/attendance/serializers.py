from rest_framework import serializers
from students.serializers import StudentSerializer
from courses.serializers import CourseSerializer
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = ["id", "student", "course", "date", "status"]
