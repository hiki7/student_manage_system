from rest_framework import serializers
from .models import Student
from users.serializers import UserSerializer


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ["id", "user", "dob", "registration_date"]
