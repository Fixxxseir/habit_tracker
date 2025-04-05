from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Habit(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        verbose_name=_("Пользователь"),
        on_delete=models.CASCADE,
        related_name="habits",
        help_text="Пользователь"
    )
    location = models.CharField(
        verbose_name=_("Место выполнения привычки"),
        max_length=255,
        null=True,
        blank=True,
        help_text="Введите место для выполнения привычки"
    )
    time = models.TimeField(
        verbose_name=_("Время выполнения привычки"),
        null=True,
        blank=True,
        help_text="Введите время выполнения привычки")
    action = models.CharField(
        verbose_name=_("Действие"),
        max_length=255,
        help_text="Введите действие")
    is_positive_habit = models.BooleanField(
        verbose_name=_("Положительная привычка"),
        default=False,
        help_text="Признак положительной привычки"
    )
    associated_habit = models.ForeignKey(
        'self',
        verbose_name=_("Связанная привычка"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_habits",
        help_text="Связанная привычка для полезных привычек"
    )
    periodicity = models.PositiveIntegerField(
        verbose_name=_("Периодичность"),
        default=1,
        help_text="Периодичность выполнения"
    )
    reward = models.CharField(
        verbose_name=_("Вознаграждение"),
        max_length=255,
        null=True,
        blank=True,
        help_text="Введите вознаграждение"
    )
    time_to_complete = models.PositiveIntegerField(
        verbose_name=_("Время выполнения"),
        help_text="Введите время выполнения привычки"
    )
    is_published = models.BooleanField(
        verbose_name=_("Статус публичности"),
        default=False,
        help_text="Выберите статус публичности"
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f'Привычка {self.action} пользователя: {self.user.username}'
