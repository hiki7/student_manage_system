from rest_framework.viewsets import ModelViewSet
from .models import Grade
from .serializers import GradeSerializer
from rest_framework.permissions import IsAuthenticated


class GradeViewSet(ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]
