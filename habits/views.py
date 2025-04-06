from django.db.models import Q
from loguru import logger
from rest_framework import viewsets, permissions
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
            return models.Habit.objects.all()
        return models.Habit.objects.filter(
            Q(user=user) | Q(is_published=True)
        )

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated,
                                  OwnerHabitPermission | IsAdminOrIsStaff]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated,
                                  OwnerHabitPermission]
        else:
            permission_classes = [permissions.IsAuthenticated,
                                  (OwnerHabitPermission | IsAdminOrIsStaff)]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Возвращает сериализатор в зависимости от действия.
        """
        if self.action == 'retrieve':
            return serializers.HabitSerializer
        elif self.action in ['create', 'update', 'partial_update']:
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
