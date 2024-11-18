from rest_framework import serializers
from .models import Course, Enrollment
from users.serializers import UserSerializer
from students.serializers import StudentSerializer


class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ["id", "name", "description", "instructor"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["instructor"] = request.user
        return super().create(validated_data)


class EnrollmentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ["id", "student", "course", "enrollment_date"]
