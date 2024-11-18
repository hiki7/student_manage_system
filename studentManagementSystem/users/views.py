from rest_framework.viewsets import ModelViewSet
from .models import CustomUser
from .permissions import IsStudent, IsAdmin
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            return [IsAuthenticated(), IsStudent() or IsAdmin()]
        elif self.action in ["retrieve"]:
            return [IsAuthenticated(), IsStudent() or IsAdmin()]
        elif self.action in ["list", "destroy"]:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == "student":
            return CustomUser.objects.filter(id=user.id)
        return super().get_queryset()
