# ai/services.py
import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from datetime import timedelta
from .utils import get_llm_response, safe_json_parse
from .prompts import COURSE_ANALYSIS_PROMPT, STRATEGY_GENERATION_PROMPT

class CourseAnalyzer:
    def parse_stepik_course(self, course_url):
        """Упрощенный парсинг Stepik"""
        try:
            # Базовая информация из URL
            return f"""
            Ссылка на курс: {course_url}
            Платформа: Stepik
            Для детального анализа требуется доступ к API Stepik
            """
        except Exception as e:
            return f"Ошибка парсинга: {e}"

    def analyze_course_with_llm(self, raw_course_content):
        """Анализ курса с помощью локальной LLM"""
        print("🔍 Анализируем курс с помощью LLM...")
        llm_response = get_llm_response(
            system_prompt=COURSE_ANALYSIS_PROMPT,
            user_prompt=f"Данные курса: {raw_course_content}"
        )
        
        if llm_response:
            parsed_data = safe_json_parse(llm_response)
            if parsed_data and 'error' not in parsed_data:
                print("✅ Анализ курса завершен успешно")
                return parsed_data
        
        print("🔄 Используем резервный анализ курса")
        return self.get_fallback_course_analysis()

    def get_fallback_course_analysis(self):
        """Резервный анализ курса"""
        return {
            "title": "Образовательный курс",
            "description": "Курс для развития навыков и знаний в выбранной области",
            "topics": [
                {
                    "title": "Основы и введение",
                    "complexity": "beginner", 
                    "estimated_study_time_hours": 3,
                    "key_concepts": ["базовые понятия", "терминология", "основные принципы"]
                },
                {
                    "title": "Практическое применение",
                    "complexity": "intermediate",
                    "estimated_study_time_hours": 5,
                    "key_concepts": ["решение задач", "анализ кейсов", "практические навыки"]
                }
            ],
            "total_estimated_hours": 8,
            "primary_skills": ["аналитическое мышление", "решение проблем", "критическое мышление"]
        }

    def full_analysis(self, course_url):
        """Полный анализ курса"""
        print(f"🔍 Начинаем анализ курса: {course_url}")
        raw_content = self.parse_stepik_course(course_url)
        structured_data = self.analyze_course_with_llm(raw_content)
        return structured_data

class StrategyGenerator:
    def generate_study_strategy(self, course_analysis, user_profile):
        """Генерация учебного плана"""
        print("🎯 Генерируем учебный план...")
        
        llm_response = get_llm_response(
            system_prompt=STRATEGY_GENERATION_PROMPT,
            user_prompt="Сгенерируй учебный план"
        )
        
        if llm_response:
            strategy_data = safe_json_parse(llm_response)
        else:
            print("🔄 Используем резервный учебный план")
            strategy_data = self.get_fallback_strategy()
        
        # Добавляем метаданные
        strategy_data['generated_at'] = timezone.now().isoformat()
        strategy_data['profile_used'] = user_profile
        
        return self.calculate_deadlines(strategy_data)

    def get_fallback_strategy(self):
        """Резервный учебный план"""
        return {
            "weekly_schedule": [
                {
                    "week_number": 1,
                    "topics_to_cover": ["Основы и введение"],
                    "study_goals": "Ознакомиться с базовыми понятиями и терминологией курса",
                    "activities": [
                        {
                            "type": "theory",
                            "description": "Изучить вводные материалы и основные концепции",
                            "deadline": "2024-01-15",
                            "xp_reward": 50
                        },
                        {
                            "type": "practice", 
                            "description": "Выполнить упражнения на закрепление материала",
                            "deadline": "2024-01-17",
                            "xp_reward": 30
                        }
                    ],
                    "total_xp": 80
                }
            ],
            "total_estimated_weeks": 4,
            "final_deadline": "2024-02-15",
            "learning_strategy": "Поэтапное изучение с регулярной практикой и повторением"
        }

    def calculate_deadlines(self, strategy_data):
        """Расчет дедлайнов"""
        start_date = timezone.now().date()
        total_weeks = strategy_data.get('total_estimated_weeks', 1)
        
        strategy_data['final_deadline'] = (
            start_date + timedelta(weeks=total_weeks)
        ).isoformat()
        
        # Обновляем дедлайны в weekly_schedule
        for week in strategy_data.get('weekly_schedule', []):
            week_number = week['week_number']
            week_deadline = start_date + timedelta(weeks=week_number)
            for activity in week.get('activities', []):
                if 'deadline' not in activity:
                    activity['deadline'] = week_deadline.isoformat()
        
        return strategy_data