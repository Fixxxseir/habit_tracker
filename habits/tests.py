from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from habits.models import Habit
from users.models import User

User = get_user_model()


class HabitTestCase(TestCase):
    """
    Тесты endpoint, permissions, validators
    """
    def setUp(self):
        self.client = APIClient()

        # Администратор
        self.admin_user = User.objects.create(
            email="admin@example.com", is_staff=True, is_superuser=True
        )
        self.admin_user.set_password("adminpass")
        self.admin_user.save()
        self.client.force_authenticate(user=self.admin_user)

        self.user_1 = User.objects.create(
            email="user@example.com",
            tg_username="test_user",
            tg_chat_id="12345",
        )
        self.user_1.set_password("user1")
        self.user_1.save()

        self.user_2 = User.objects.create(
            email="other@example.com",
            tg_username="other_user",
            tg_chat_id="54321",
        )
        self.user_2.set_password("user2")
        self.user_2.save()

        # Привычки для тестов
        self.habit1 = Habit.objects.create(
            user=self.user_1,
            location="Дома",
            action="Чтение книги",
            time_to_complete=120,
            is_published=True,
        )

        self.habit2 = Habit.objects.create(
            user=self.user_1,
            location="Парк",
            action="Пробежка",
            time_to_complete=120,
            is_published=False,
        )

        self.habit3 = Habit.objects.create(
            user=self.user_2,
            location="Спортзал",
            action="Тренировка",
            time_to_complete=120,
            is_published=True,
        )
        self.habit3 = Habit.objects.create(
            user=self.user_2,
            location="Бассейн",
            action="Плавание",
            time_to_complete=120,
            is_published=False,
        )

    def test_habit_list_admin(self):
        response = self.client.get(reverse("habits:habit-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 4)

    def test_habit_list_user(self):
        self.client.logout()
        self.client.force_authenticate(self.user_1)
        response = self.client.get(reverse("habits:habit-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_habit_detail_admin(self):
        response = self.client.get(
            reverse("habits:habit-detail", args=[self.habit1.id])
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_habit_detail_owner(self):
        self.client.logout()
        self.client.force_authenticate(self.user_1)
        response = self.client.get(
            reverse("habits:habit-detail", args=[self.habit1.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_update_admin(self):
        data = {"action": "Updated by admin"}
        response = self.client.patch(
            reverse("habits:habit-detail", args=[self.habit1.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_habit_update_owner(self):
        self.client.logout()
        self.client.force_authenticate(self.user_1)
        data = {"action": "Updated by owner"}
        response = self.client.patch(
            reverse("habits:habit-detail", args=[self.habit1.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_update_other_user(self):
        self.client.logout()
        self.client.force_authenticate(self.user_2)
        data = {"action": "Try to update"}
        response = self.client.patch(
            reverse("habits:habit-detail", args=[self.habit1.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_habit_delete_admin(self):
        response = self.client.delete(
            reverse("habits:habit-detail", args=[self.habit1.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_habit_delete_owner(self):
        response = self.client.delete(
            reverse("habits:habit-detail", args=[self.habit1.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_habit_delete_other_user(self):
        self.client.logout()
        self.client.force_authenticate(self.user_2)
        response = self.client.delete(
            reverse("habits:habit-detail", args=[self.habit1.id])
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_associated_habit_validation(self):
        self.client.logout()
        self.client.force_authenticate(self.user_1)
        habit = Habit.objects.create(
            user=self.user_1,
            action="Медитация",
            is_positive_habit=False,
            time_to_complete=120,
        )

        data = {
            "action": "Полезная привычка",
            "associated_habit": habit.id,
            "time_to_complete": 120,
        }
        response = self.client.post(reverse("habits:habit-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Связанная привычка должна быть приятной", str(response.data)
        )

    def test_reward_and_associated_habit_validation(self):
        self.client.logout()
        self.client.force_authenticate(self.user_2)
        habit = Habit.objects.create(
            user=self.user_2,
            action="Полезная привычка",
            is_positive_habit=False,
            time_to_complete=120,
        )

        data = {
            "action": "Новая привычка",
            "associated_habit": habit.id,
            "reward": "Шоколадка",
            "time_to_complete": 120,
        }
        response = self.client.post(reverse("habits:habit-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Одновременный выбор связанной привычки и вознаграждения запрещен",
            str(response.data),
        )

    def test_time_to_complete_validation(self):
        self.client.logout()
        self.client.force_authenticate(self.user_2)
        data = {"action": "Долгая привычка", "time_to_complete": 130}
        response = self.client.post(reverse("habits:habit-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Время выполнения не более 120 секунд", str(response.data)
        )

    def test_positive_habit_only_validator(self):
        self.client.logout()
        self.client.force_authenticate(self.user_1)

        data = {
            "action": "Чииииллл",
            "is_positive_habit": True,
            "reward": "чил + чил",
            "time_to_complete": 120,
        }
        response = self.client.post(reverse("habits:habit-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "У приятной привычки не может быть вознаграждения"
            "или связанной привычки",
            str(response.data),
        )

        associated_habit = Habit.objects.create(
            user=self.user_1,
            action="Связанная привычка",
            is_positive_habit=False,
            time_to_complete=120,
        )
        data["associated_habit"] = associated_habit.id
        response = self.client.post(reverse("habits:habit-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "У приятной привычки не может быть вознаграждения"
            "или связанной привычки",
            str(response.data),
        )

    def test_frequency_of_habit_validator(self):
        self.client.logout()
        self.client.force_authenticate(self.user_1)

        data = {
            "action": "Неправильная частота",
            "time_to_complete": 120,
            "periodicity": 0,
        }
        response = self.client.post(reverse("habits:habit-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Нельзя выполнять привычку реже, чем 1 раз в 7 дней",
            str(response.data),
        )

        data["periodicity"] = 8
        response = self.client.post(reverse("habits:habit-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Нельзя выполнять привычку реже, чем 1 раз в 7 дней",
            str(response.data),
        )

        data["periodicity"] = 3
        response = self.client.post(reverse("habits:habit-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
