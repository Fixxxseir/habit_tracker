from rest_framework import serializers


class BaseValidator:
    """
    Базовый класс валидатора для того что бы не дублировать логику
    """

    def __init__(self, *fields):
        self.fields = fields

    def __call__(self, value):
        """
        Извлекает указанные поля из данных и передает в метод validate.
        """
        field_values = {field: value.get(field) for field in self.fields}
        self.validate(**field_values)

    def validate(self, **kwargs):
        """
        Метод который должен быть реализован у других классов
        """
        raise NotImplementedError(
            "Метод validate должен быть реализован" " в подклассе."
        )


class AssociatedHabitOrRewardValidator(BaseValidator):
    """
    Проверяет, что не указаны одновременно связанная привычка и вознаграждение
    """

    def validate(self, associated_habit, reward, **kwargs):
        if associated_habit and reward:
            raise serializers.ValidationError(
                "Одновременный выбор связанной привычки"
                " и вознаграждения запрещен"
            )


class ExecutionTimeLimitValidator(BaseValidator):
    """
    Проверяет, что время выполнения не превышает 120 секунд
    """

    def validate(self, time_to_complete, **kwargs):
        if time_to_complete and time_to_complete > 120:
            raise serializers.ValidationError(
                "Время выполнения не более 120 секунд"
            )


class RelatedHabitValidator(BaseValidator):
    """
    Проверяет, что связанная привычка является приятной
    """

    def validate(self, associated_habit, **kwargs):
        if associated_habit and not associated_habit.is_positive_habit:
            raise serializers.ValidationError(
                "Связанная привычка должна быть приятной"
            )


class PositiveHabitOnlyValidator(BaseValidator):
    """
    Проверяет, что у приятной привычки нет вознаграждения
    или связанной привычки
    """

    def validate(self, is_positive_habit, reward, associated_habit, **kwargs):
        if is_positive_habit and (reward or associated_habit):
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения"
                "или связанной привычки"
            )


class FrequencyOfHabitValidator(BaseValidator):
    """
    Проверяет, что привычка выполняется не реже 1 раза в 7 дней
    """

    def validate(self, periodicity, **kwargs):
        if periodicity is not None and not (1 <= periodicity <= 7):
            raise serializers.ValidationError(
                "Нельзя выполнять привычку реже, чем 1 раз в 7 дней"
            )
