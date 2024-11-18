from celery import shared_task
from django.core.mail import send_mail
from users.models import CustomUser

@shared_task
def send_attendance_reminder():
    students = CustomUser.objects.filter(role='student')
    for student in students:
        send_mail(
            subject="Daily Attendance Reminder",
            message="Please remember to mark your attendance for today.",
            from_email="admin@school.com",
            recipient_list=[student.email],
        )
    return f"Sent attendance reminders to {students.count()} students."
