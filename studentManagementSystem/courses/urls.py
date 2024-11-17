from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, EnrollmentViewSet

router = DefaultRouter()

router.register("", CourseViewSet)
router.register("", EnrollmentViewSet)

urlpatterns = router.urls
