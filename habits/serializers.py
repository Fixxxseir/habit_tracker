from rest_framework import serializers

from habits.models import Habit
from habits.validators import (
    AssociatedHabitOrRewardValidator,
    ExecutionTimeLimitValidator,
    FrequencyOfHabitValidator,
    PositiveHabitOnlyValidator,
    RelatedHabitValidator,
)


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
        read_only_fields = (
            "id",
            "user",
        )


class HabitCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания
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
        validators = [
            AssociatedHabitOrRewardValidator("associated_habit", "reward"),
            ExecutionTimeLimitValidator("time_to_complete"),
            RelatedHabitValidator("associated_habit"),
            PositiveHabitOnlyValidator(
                "is_positive_habit", "reward", "associated_habit"
            ),
            FrequencyOfHabitValidator("periodicity"),
        ]
