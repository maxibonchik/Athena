# courses/services/course_importer.py

from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from django.utils.crypto import get_random_string
from courses.models import Course, CourseModule, CourseLesson


def _make_unique_username(base: str, User):
    """
    Попытки с суффиксами, чтобы получить свободный username.
    Возвращает уникальный username (строго не вызывает исключений).
    """
    base = base[:150]  # safety
    username = base
    i = 0
    while User.objects.filter(username=username).exists():
        i += 1
        username = f"{base}{i}"
    return username


class CourseImporter:
    """
    Импортирует структуру парсера Stepik в базу данных Django.
    Обеспечивает безопасное создание/получение автора (не падает на unique-constraint).
    """

    def __init__(self, default_author_email="admin@example.com"):
        User = get_user_model()

        # 1) Сначала пробуем найти автора по email
        self.author = User.objects.filter(email=default_author_email).first()
        if self.author:
            return

        # 2) Если не нашли — подбираем уникальный username и создаём обычного пользователя
        base = default_author_email.split("@")[0]
        username = _make_unique_username(base, User)

        # создаём пользователя безопасно (create_user хеширует пароль)
        # ставим случайный пароль, user не будет суперюзером по умолчанию
        password = get_random_string(16)
        try:
            self.author = User.objects.create_user(
                username=username,
                email=default_author_email,
                password=password,
                is_staff=False,
                is_superuser=False,
            )
        except IntegrityError:
            # На всякий случай — если race condition, подберём другой username
            username = _make_unique_username(base + get_random_string(4), User)
            self.author = User.objects.create_user(
                username=username,
                email=default_author_email,
                password=get_random_string(16),
                is_staff=False,
                is_superuser=False,
            )

    @transaction.atomic
    def import_course(self, parsed_data: dict) -> Course:
        """
        Создание курса + модулей + уроков в транзакции.
        parsed_data ожидается в формате, который отдаёт StepikParser.
        """
        # 1) Создаём курс
        course = Course.objects.create(
            title=parsed_data.get("title", "Untitled"),
            author=self.author
        )

        # 2) Создаём модули и уроки
        for m_index, module_data in enumerate(parsed_data.get("modules", []), start=1):
            module = CourseModule.objects.create(
                course=course,
                title=module_data.get("title", f"Module {m_index}"),
                order=m_index
            )

            for l_index, lesson_data in enumerate(module_data.get("lessons", []), start=1):
                CourseLesson.objects.create(
                    module=module,
                    title=lesson_data.get("title", f"Lesson {l_index}"),
                    content=lesson_data.get("summary", "") or "",
                    order=l_index
                )

        return course

