from django.core.cache import cache
import pytest
from rest_framework.test import APIClient
from users.models import CustomUser
from students.models import Student
from rest_framework.status import HTTP_200_OK


@pytest.mark.django_db
def test_student_cache():
    """
    Test that student data is cached after the first request.
    """
    student_user = CustomUser.objects.create(username="student1", role="student")
    student = Student.objects.create(
        user=student_user, dob="2000-01-01", registration_date="2023-11-01"
    )
    client = APIClient()
    client.force_authenticate(user=student_user)

    cache.clear()

    cache_key = f"student_profile_{student.id}"
    assert cache.get(cache_key) is None

    response = client.get(f"/api/students/{student.id}/")
    assert response.status_code == HTTP_200_OK
    assert cache.get(cache_key) is not None

    cached_data = cache.get(cache_key)
    response = client.get(f"/api/students/{student.id}/")
    assert response.status_code == HTTP_200_OK
    assert cached_data is not None
    assert cached_data.id == student.id
