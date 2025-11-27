# courses/services/stepik_parser.py

from .stepik_client import StepikClient


class StepikParser:
    """
    Парсер курса Stepik.
    Получает:
     - информацию о курсе
     - секции (если есть)
     - units → уроки
     - уроки со summary
    Возвращает готовый JSON для записи в базу.
    """

    def __init__(self):
        self.client = StepikClient()

    def parse_course(self, course_id) -> dict:
        """
        Основной метод: собирает ВСЮ структуру курса в единый JSON.
        """

        # 1) Получаем данные курса
        course_data = self.client.get_course(course_id)
        course = course_data.get("courses", [None])[0]

        if not course:
            raise ValueError(f"Курс с ID {course_id} не найден")

        title = course.get("title", "")
        description = course.get("description", "")

        # 2) Получаем units (они связывают sections и lessons)
        units_resp = self.client.get_units(course_id)
        units = units_resp.get("units", [])

        # Собираем уникальные section_id
        all_section_ids = {u["section"] for u in units if u.get("section")}

        # 3) Пытаемся получить секции через Stepik API
        sections_resp = self.client.get_sections(course_id)
        sections = sections_resp.get("sections", [])

        # ----
        # ВАЖНО: Stepik может НЕ отдавать список секций.
        # Тогда мы создадим их вручную по section_id.
        # ----
        if not sections:
            print("⚠️ Stepik API не вернул sections — создаём виртуальную структуру.")
            sections = [
                {
                    "id": sid,
                    "title": f"Section {sid}",
                    "position": i + 1
                }
                for i, sid in enumerate(sorted(all_section_ids))
            ]

        # 4) Формируем соответствие: section_id → list(lesson_id)
        section_to_lessons = {}

        for unit in units:
            section_id = unit.get("section")
            lesson_id = unit.get("lesson")

            if not section_id or not lesson_id:
                continue

            section_to_lessons.setdefault(section_id, []).append(lesson_id)

        # 5) Получаем все уроки
        all_lesson_ids = []
        for lesson_list in section_to_lessons.values():
            all_lesson_ids.extend(lesson_list)

        all_lesson_ids = list(set(all_lesson_ids))

        lessons_resp = self.client.get_lessons(all_lesson_ids)
        lessons = {lesson["id"]: lesson for lesson in lessons_resp.get("lessons", [])}

        # 6) Собираем финальные модули
        modules = []

        for section in sections:
            section_id = section["id"]

            module = {
                "id": section_id,
                "title": section.get("title", ""),
                "position": section.get("position", 0),
                "lessons": []
            }

            lesson_ids = section_to_lessons.get(section_id, [])

            for lid in lesson_ids:
                lesson = lessons.get(lid)
                if not lesson:
                    continue

                module["lessons"].append({
                    "id": lesson["id"],
                    "title": lesson.get("title", ""),
                    "summary": lesson.get("summary", ""),
                    "position": lesson.get("position", 0),
                    "steps": []  # сюда добавим позже шаги урока (контент)
                })

            modules.append(module)

        # сортировка
        modules = sorted(modules, key=lambda m: m["position"])

        # 7) Собираем итоговый JSON
        return {
            "original_course_id": course_id,
            "title": title,
            "description": description,
            "modules": modules,
        }
