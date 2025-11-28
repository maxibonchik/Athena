# courses/services/course_importer.py

from django.contrib.auth import get_user_model
from courses.models import Course, CourseModule, CourseLesson


class CourseImporter:
    """
    Импортирует структуру парсера Stepik в базу данных Django.
    """

    def __init__(self, default_author_email="admin@example.com"):
        # Автор курса — временно админ (или любой пользователь)
        User = get_user_model()
        self.author, _ = User.objects.get_or_create(
            email=default_author_email,
            defaults={"username": default_author_email.split("@")[0]},
        )

    def import_course(self, parsed_data: dict) -> Course:
        """
        Создание курса + модулей + уроков
        """

        # 1) Создаём курс
        course = Course.objects.create(
            title=parsed_data["title"],
            author=self.author
        )

        # 2) Создаём модули
        for m_index, module_data in enumerate(parsed_data["modules"], start=1):
            module = CourseModule.objects.create(
                course=course,
                title=module_data["title"],
                order=m_index
            )

            # 3) Уроки внутри модуля
            for l_index, lesson_data in enumerate(module_data["lessons"], start=1):
                CourseLesson.objects.create(
                    module=module,
                    title=lesson_data["title"],
                    content=lesson_data.get("summary", "") or "",
                    order=l_index
                )

        return course
