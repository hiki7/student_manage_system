import pytest
from rest_framework.test import APIClient
from users.models import CustomUser
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_course_create_permission_as_teacher():
    """
    Test that a teacher can create a course.
    """
    teacher_user = CustomUser.objects.create(username="teacher1", role="teacher")
    client = APIClient()
    client.force_authenticate(user=teacher_user)
    payload = {
        "name": "Math 101",
        "description": "Basic Math Course",
    }
    response = client.post("/api/courses/", payload)
    assert response.status_code == 201
    assert response.data["instructor"]["username"] == teacher_user.username


@pytest.mark.django_db
def test_course_create_permission_as_student():
    """
    Test that a student cannot create a course.
    """
    student_user = CustomUser.objects.create(username="student1", role="student")
    client = APIClient()
    client.force_authenticate(user=student_user)
    payload = {"name": "Math 101", "description": "Basic Math Course"}
    response = client.post("/api/courses/", payload)
    assert response.status_code == HTTP_403_FORBIDDEN
