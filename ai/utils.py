# ai/utils.py
from transformers import pipeline
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class LocalLLM:
    def __init__(self):
        self.generator = None
        
    def load_model(self):
        """Загружаем легкую модель для генерации"""
        try:
            # Используем маленькую русскоязычную модель
            model_name = "IlyaGusev/rugpt3medium_sum_gazeta"
            self.generator = pipeline(
                "text-generation",
                model=model_name,
                tokenizer=model_name,
                device=-1  # CPU
            )
            print("✅ Модель успешно загружена")
            return True
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            print(f"❌ Ошибка загрузки модели: {e}")
            return False
    
    def generate_response(self, system_prompt, user_prompt, max_length=500):
        """Генерация ответа с помощью локальной модели"""
        if not self.generator:
            if not self.load_model():
                return self.generate_fallback_response(system_prompt, user_prompt)
        
        try:
            prompt = f"{system_prompt}\n\n{user_prompt}\n\nОтвет:"
            
            result = self.generator(
                prompt,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=50256
            )
            
            response = result[0]['generated_text'].replace(prompt, "").strip()
            print(f"✅ Сгенерирован ответ: {response[:100]}...")
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            print(f"❌ Ошибка генерации: {e}")
            return self.generate_fallback_response(system_prompt, user_prompt)

    def generate_fallback_response(self, system_prompt, user_prompt):
        """Резервная генерация ответов"""
        print("🔄 Используем резервный генератор")
        
        if "анализ курса" in system_prompt.lower():
            return json.dumps({
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
                    },
                    {
                        "title": "Продвинутые темы",
                        "complexity": "advanced", 
                        "estimated_study_time_hours": 4,
                        "key_concepts": ["углубленное изучение", "экспертные знания"]
                    }
                ],
                "total_estimated_hours": 12,
                "primary_skills": ["аналитическое мышление", "решение проблем", "критическое мышление"]
            }, ensure_ascii=False)
            
        elif "учебный план" in system_prompt.lower():
            return json.dumps({
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
                    },
                    {
                        "week_number": 2,
                        "topics_to_cover": ["Практическое применение"],
                        "study_goals": "Научиться применять полученные знания на практике",
                        "activities": [
                            {
                                "type": "practice",
                                "description": "Решить практические задачи и кейсы",
                                "deadline": "2024-01-22",
                                "xp_reward": 70
                            }
                        ],
                        "total_xp": 70
                    }
                ],
                "total_estimated_weeks": 3,
                "final_deadline": "2024-01-29",
                "learning_strategy": "Поэтапное изучение с регулярной практикой и повторением"
            }, ensure_ascii=False)
        else:
            return '{"status": "success", "message": "Запрос обработан"}'

# Глобальный инстанс
local_llm = LocalLLM()

def get_llm_response(system_prompt, user_prompt, model="local"):
    """
    Универсальная функция для работы с LLM
    """
    print(f"🎯 Запрос к LLM: {system_prompt[:100]}...")
    return local_llm.generate_response(system_prompt, user_prompt)

def safe_json_parse(json_string):
    """Безопасный парсинг JSON"""
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        logger.warning(f"JSON decode error: {e}")
        print(f"❌ Ошибка парсинга JSON: {e}")
        # Пытаемся исправить JSON
        try:
            # Убираем возможные лишние символы
            json_string = json_string.strip()
            if json_string.startswith('```json'):
                json_string = json_string[7:]
            if json_string.endswith('```'):
                json_string = json_string[:-3]
            return json.loads(json_string)
        except:
            return {"error": "Невалидный JSON", "raw_response": json_string[:200]}