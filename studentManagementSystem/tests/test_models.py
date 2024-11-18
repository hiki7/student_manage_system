import datetime
import pytest
from students.models import Student
from users.models import CustomUser


@pytest.mark.django_db
def test_student_creation():
    """
    Test the creation of a Student instance.
    """
    user = CustomUser.objects.create(username="student1", role="student")
    student = Student.objects.create(
        user=user,
        dob=datetime.date(2000, 1, 1),
    )
    assert student.user.username == "student1"
    assert student.dob == datetime.date(2000, 1, 1)
    assert student.registration_date == datetime.date.today()
