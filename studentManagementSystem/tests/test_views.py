from rest_framework.test import APIClient
import pytest
from students.models import Student
from users.models import CustomUser
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_student_list_as_admin():
    """
    Test that an admin can view the list of students.
    """
    admin_user = CustomUser.objects.create(username="admin", role="admin")
    client = APIClient()
    client.force_authenticate(user=admin_user)
    response = client.get("/api/students/")
    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_student_list_as_student():
    """
    Test that a student can only view their own record.
    """
    student_user = CustomUser.objects.create(username="student1", role="student")
    student = Student.objects.create(
        user=student_user, dob="2000-01-01", registration_date="2023-11-01"
    )
    client = APIClient()
    client.force_authenticate(user=student_user)
    response = client.get("/api/students/")
    assert response.status_code == HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == student.id
