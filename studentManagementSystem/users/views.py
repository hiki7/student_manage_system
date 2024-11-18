from rest_framework.viewsets import ModelViewSet
from .models import CustomUser
from .permissions import IsStudent, IsAdmin
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger("custom")


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
            logger.info(f"Student {user.username} is accessing their own profile.")
            return CustomUser.objects.filter(id=user.id)
        logger.info(f"Admin {user.username} is accessing the user list.")
        return super().get_queryset()

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        logger.info(
            f"User {request.user.username} is retrieving profile of {user.username}."
        )
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        logger.info(
            f"User {request.user.username} is updating profile of {user.username}."
        )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        logger.info(
            f"User {request.user.username} is partially updating profile of {user.username}."
        )
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        logger.warning(
            f"Admin {request.user.username} is deleting profile of {user.username}."
        )
        return super().destroy(request, *args, **kwargs)
