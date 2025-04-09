import requests
from celery import shared_task
from django.utils import timezone
from loguru import logger

from . import services
from .models import Habit


@shared_task
def send_habit_notifications():
    """
    Отправка уведомлений о привычках,
    которые должны быть выполнены в данное время.
    """

    now = timezone.localtime(timezone.now())
    current_time = now.time()
    logger.info(f"Текущее время: {current_time}")

    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute,
        user__is_active=True,
    ).select_related("user")
    logger.info(f"Найденные привычки: {habits}")
    habits_1 = Habit.objects.all()
    for habit in habits_1:
        logger.info(f"Найдена привычка: {habit.action}, время: {habit.time}")

    if not habits.exists():
        logger.info("Нет привычек для отправки уведомлений в текущее время.")
        return

    for habit in habits:
        try:

            if (
                    not hasattr(habit.user, "tg_chat_id")
                    or not habit.user.tg_chat_id
            ):
                logger.warning(
                    f"У пользователя {habit.user.username} отсутствует tg_chat_id"
                )
                continue

            message = (
                f"Напоминание: Выполните привычку '{habit.action}' в '{habit.location}' "
                f"время выполнения: {habit.time.strftime('%H:%M')}. "
                f"Вознаграждение: {habit.reward if habit.reward else 'Без вознаграждения'}."
            )

            services.send_telegram_message(message, habit.user.tg_chat_id)

            logger.info(
                f"Уведомление отправлено пользователю {habit.user.email}"
                f" о привычке '{habit.action}'."
            )

        except Exception as e:
            logger.error(
                f"Ошибка при отправке уведомления пользователю {habit.user.username}: {e}"
            )


@shared_task
def check_internet():
    """
    Проверка
    """
    try:
        response = requests.get("https://api.telegram.org", timeout=5)
        return f"Status: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

# ОШИБКА РАБОТЫ C REDIS, ВОЗМОНЖ ПОМОЖЕТ DOCKER
# @shared_task
# def send_habit_notifications():
#     """
#     Отправка уведомлений о привычках, которые должны быть выполнены в данное время.
#     """
#     now = timezone.now()
#     current_time = now.time()
#
#     cache_key = f'habits_to_notify_{current_time}'
#     habits = cache.get(cache_key)
#
#     if habits is None:
#         habits = Habit.objects.filter(
#             time=current_time,
#             user__is_active=True
#         ).select_related('user')
#
#         cache.set(cache_key, habits, timeout=3600)
#
#     if not habits.exists():
#         logger.info("Нет привычек для отправки уведомлений в текущее время.")
#         return
#
#     for habit in habits:
#         try:
#             if not hasattr(habit.user, 'tg_chat_id') or not habit.user.tg_chat_id:
#                 logger.warning(f"У пользователя {habit.user.username} отсутствует tg_chat_id")
#                 continue
#
#             message = (
#                 f"Напоминание: Выполните привычку '{habit.action}' в '{habit.location}' "
#                 f"время выполнения: {habit.time.strftime('%H:%M')}. "
#                 f"Вознаграждение: {habit.reward if habit.reward else 'Без вознаграждения'}."
#             )
#
#             services.send_telegram_message(habit.user.tg_chat_id, message)
#
#             logger.info(f"Уведомление отправлено пользователю {habit.user.username} о привычке '{habit.action}'.")
#
#         except Exception as e:
#             logger.error(f"Ошибка при отправке уведомления пользователю {habit.user.username}: {e}")
