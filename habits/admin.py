from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """
    Регистрация модели в админ панели
    """

    list_display = (
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
