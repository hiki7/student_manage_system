from celery import shared_task
from django.core.mail import send_mail
from users.models import CustomUser


@shared_task
def send_attendance_reminder():
    students = CustomUser.objects.filter(role="student")
    for student in students:
        send_mail(
            subject="Daily Attendance Reminder",
            message="Please remember to mark your attendance for today.",
            from_email="admin@school.com",
            recipient_list=[student.email],
        )
    return f"Sent attendance reminders to {students.count()} students."


@shared_task
def send_grade_update_notification(student_email, course_name, grade):
    send_mail(
        subject="Grade Update Notification",
        message=f"Your grade for the course {course_name} has been updated to {grade}.",
        from_email="admin@school.com",
        recipient_list=[student_email],
    )
    return f"Sent grade update notification to {student_email}."
