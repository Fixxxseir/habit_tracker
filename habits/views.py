from loguru import logger
from rest_framework import viewsets, permissions
from habits import models, serializers


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HabitSerializer
    lookup_field = "pk"
    lookup_url_kwarg = "habit_id"
    permission_classes = [permissions.IsAuthenticated]

