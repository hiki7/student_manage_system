from rest_framework import serializers
from users.serializers import UserSerializer
from students.serializers import StudentSerializer
from courses.serializers import CourseSerializer
from .models import Grade


class GradeSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    teacher = UserSerializer(read_only=True)

    class Meta:
        model = Grade
        fields = ["id", "student", "course", "grade", "teacher", "date"]
