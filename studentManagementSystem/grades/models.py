from django.db import models


class Grade(models.Model):
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE)
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)
    teacher = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
