from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор представления
    """

    class Meta:
        model = Habit
        fields = (
            "id",
            "user",
            "location",
            "time",
            "action",
            "is_positive_habit",
            "associated_habit",
            "periodicity",
            "reward",
            "time_to_complete",
            "is_published",
        )
        read_only_fields = ("id", "user",)


class HabitCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор соаздния
    """
    class Meta:
        model = Habit
        fields = (
            "location",
            "time",
            "action",
            "is_positive_habit",
            "associated_habit",
            "periodicity",
            "reward",
            "time_to_complete",
            "is_published",
        )

