# Краткое описание задачи
В рамках данного проекта необходимо разработать систему управления привычками, которая будет включать в себя следующие ключевые компоненты:

## Модели
Создание модели "Привычка", которая будет содержать следующие поля:

- Пользователь: владелец привычки.
- Место: где привычка будет выполняться.
- Время: когда привычка должна выполняться.
- Действие: само действие привычки.
- Связанные привычки: возможность указания приятной привычки, которая связана с полезной привычкой.
- Периодичность: частота выполнения привычки (по умолчанию — ежедневно).
- Вознаграждение: что пользователь получит за выполнение привычки.
- Время на выполнение: предполагаемое время для выполнения привычки (не более 120 секунд).
- Признак публичности: возможность делиться привычками с другими пользователями.
# Валидация
- Необходимо исключить одновременный выбор связанной привычки и указания вознаграждения.
- Привычка должна выполняться не реже одного раза в 7 дней и не должна пропускаться более 7 дней.
Приятные привычки не могут иметь вознаграждение или связанные привычки.
# Эндпоинты
Реализация следующих API-эндпоинтов для взаимодействия с фронтендом:

- Регистрация пользователей.
- Авторизация пользователей.
- Получение списка привычек текущего пользователя с пагинацией (5 привычек на страницу).
- Получение списка публичных привычек.
- Создание привычки.
- Редактирование привычки.
- Удаление привычки.
# Интеграция с Telegram
- Создание приложения для работы с Telegram, которое будет рассылать напоминания о выполнении привычек. Необходимо использовать API Telegram для отправки уведомлений.

# Безопасность
- Настройка CORS для обеспечения безопасного доступа фронтенда к API на развернутом сервере.

# Документация
- Создание документации для API, включая описание эндпоинтов, чтобы фронтенд-разработчики могли легко интегрировать их в свои экраны. Эндпоинты, которые не могут быть автоматически документированы, должны быть описаны вручную.

# Цель проекта
- Создать удобный и эффективный инструмент для пользователей, позволяющий формировать и отслеживать свои привычки, получать напоминания и делиться опытом с другими. Этот проект поможет пользователям улучшить свою продуктивность и вести более здоровый образ жизни))