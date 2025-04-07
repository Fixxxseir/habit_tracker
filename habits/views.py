from django.db.models import Q

from rest_framework import permissions, viewsets

from habits import models, serializers
from habits.permissions import IsAdminOrIsStaff, OwnerHabitPermission


class HabitViewSet(viewsets.ModelViewSet):
    """
    Вьюсет привычки
    """

    lookup_field = "pk"
    lookup_url_kwarg = "habit_id"

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return models.Habit.objects.all().order_by("-id")
        return models.Habit.objects.filter(
            Q(user=user) | Q(is_published=True)
        ).order_by("-id")

    def get_permissions(self):
        if self.action in ["list", "create"]:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ["update", "partial_update", "retrieve"]:
            permission_classes = [
                permissions.IsAuthenticated,
                OwnerHabitPermission,
            ]
        elif self.action == "destroy":
            permission_classes = [
                permissions.IsAuthenticated
                & (IsAdminOrIsStaff | OwnerHabitPermission)
            ]
        else:
            permission_classes = [
                permissions.IsAuthenticated & IsAdminOrIsStaff
            ]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Возвращает сериализатор в зависимости от действия.
        """
        if self.action in ["create", "update", "partial_update"]:
            return serializers.HabitCreateSerializer
        return serializers.HabitSerializer

    def create(self, request, *args, **kwargs):
        self.check_object_permissions(request=request, obj=None)
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.check_object_permissions(request=request, obj=None)
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
