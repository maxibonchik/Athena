# courses/services/stepik_parser.py

from .stepik_client import StepikClient

class StepikParser:
    def __init__(self):
        self.client = StepikClient()

    def parse_course(self, course_id) -> dict:
        # 1) Получаем основную информацию о курсе
        course_data = self.client.get_course(course_id)
        course = course_data.get("courses", [None])[0]

        if not course:
            raise ValueError(f"Курс с ID {course_id} не найден")

        title = course.get("title")
        description = course.get("description", "")

        # 2) Получаем sections (модули)
        sections_resp = self.client.get_sections(course_id)
        sections = sections_resp.get("sections", [])

        # 3) Получаем units — это связка modules → lessons
        units_resp = self.client.get_units(course_id)
        units = units_resp.get("units", [])

        # создаём соответствие: section_id → list(lesson_id)
        section_to_lessons = {}

        for unit in units:
            section_id = unit.get("section")
            lesson_id = unit.get("lesson")

            if not section_id or not lesson_id:
                continue

            section_to_lessons.setdefault(section_id, []).append(lesson_id)

        # 4) Получаем список всех ID уроков
        all_lesson_ids = []
        for lessons_list in section_to_lessons.values():
            all_lesson_ids.extend(lessons_list)

        # убираем дубли
        all_lesson_ids = list(set(all_lesson_ids))

        # 5) Получаем детали уроков
        lessons_resp = self.client.get_lessons(all_lesson_ids)
        lessons = {l["id"]: l for l in lessons_resp.get("lessons", [])}

        # 6) Собираем единый JSON
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

            # добавляем уроки в модуль
            for lid in lesson_ids:
                lesson = lessons.get(lid)
                if not lesson:
                    continue

                module["lessons"].append({
                    "id": lesson["id"],
                    "title": lesson.get("title", ""),
                    "summary": lesson.get("summary", ""),
                    "position": lesson.get("position", 0),
                    "steps": []  # потом будем заполнять
                })

            modules.append(module)

        # сортируем модули по позиции
        modules = sorted(modules, key=lambda m: m["position"])

        # итоговый JSON
        return {
            "original_course_id": course_id,
            "title": title,
            "description": description,
            "modules": modules,
        }
