from celery import shared_task
from django.core.mail import send_mail
from users.models import CustomUser
from attendance.models import Attendance
from grades.models import Grade
from datetime import date


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


@shared_task
def send_daily_report():
    today = date.today()

    total_attendance_records = Attendance.objects.filter(date=today).count()
    present_count = Attendance.objects.filter(date=today, status="present").count()
    attendance_percentage = (
        (present_count / total_attendance_records) * 100
        if total_attendance_records > 0
        else 0
    )

    grades = Grade.objects.all()
    total_grades = grades.count()
    average_grade = (
        sum(float(grade.grade) for grade in grades) / total_grades
        if total_grades > 0
        else 0
    )

    report = "Daily Attendance and Grade Summary:\n\n"
    report += f"Attendance: {attendance_percentage:.2f}% present.\n"
    report += f"Grades: Average score: {average_grade:.2f}.\n"

    admins = CustomUser.objects.filter(role="admin")
    for admin in admins:
        send_mail(
            subject="Daily Attendance and Grade Report",
            message=report,
            from_email="admin@school.com",
            recipient_list=[admin.email],
        )
    return f"Sent daily report to {admins.count()} admins."
