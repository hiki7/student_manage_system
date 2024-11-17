from django.db import models
from users.models import CustomUser


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="courses"
    )


class Enrollment(models.Model):
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
