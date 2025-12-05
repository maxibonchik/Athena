import json
from typing import Dict, Any

class CognitiveTestProcessor:
    """Класс для обработки результатов когнитивного теста"""
    
    # Маппинг ответов на баллы для памяти и дисциплины
    SCORE_MAP = {
        'a': 10,
        'b': 7,
        'c': 4,
        'd': 1
    }
    
    # Маппинг стилей обучения
    STYLE_MAP = {
        'a': 'visual',
        'b': 'auditory',
        'c': 'readwrite',
        'd': 'kinesthetic'
    }
    
    @classmethod
    def calculate_results(cls, form_data: Dict[str, str]) -> Dict[str, Any]:
        """Рассчитывает результаты теста"""
        
        # Подсчет стиля обучения
        style_counts = {'visual': 0, 'auditory': 0, 'readwrite': 0, 'kinesthetic': 0}
        
        for q in ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6']:
            if q in form_data:
                answer = form_data[q]
                style = cls.STYLE_MAP.get(answer)
                if style:
                    style_counts[style] += 1
        
        # Определение основного стиля
        max_count = max(style_counts.values())
        main_style = None
        
        # Если разница менее 2 - mixed
        sorted_styles = sorted(style_counts.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_styles) > 1 and (sorted_styles[0][1] - sorted_styles[1][1] < 2):
            main_style = 'mixed'
        else:
            main_style = max(style_counts, key=style_counts.get)
        
        # Подсчет баллов памяти
        memory_scores = []
        for q in ['Q7', 'Q8', 'Q9', 'Q10', 'Q11', 'Q12']:
            if q in form_data:
                score = cls.SCORE_MAP.get(form_data[q], 5)
                memory_scores.append(score)
        
        memory_avg = round(sum(memory_scores) / len(memory_scores), 1) if memory_scores else 5.0
        
        # Подсчет баллов дисциплины
        discipline_scores = []
        for q in ['Q13', 'Q14', 'Q15', 'Q16', 'Q17', 'Q18']:
            if q in form_data:
                score = cls.SCORE_MAP.get(form_data[q], 5)
                discipline_scores.append(score)
        
        discipline_avg = round(sum(discipline_scores) / len(discipline_scores), 1) if discipline_scores else 5.0
        
        # Сбор деталей
        details = {
            'style_counts': style_counts,
            'memory_scores': memory_scores,
            'discipline_scores': discipline_scores,
            'concentration_span': int(form_data.get('concentration_span', 25)),
            'preferred_study_time': form_data.get('preferred_study_time', 'evening')
        }
        
        return {
            'learning_style': main_style,
            'memory_score': memory_avg,
            'discipline_score': discipline_avg,
            'learning_style_details': details,
            'concentration_span': int(form_data.get('concentration_span', 25)),
            'preferred_study_time': form_data.get('preferred_study_time', 'evening')
        }
    
    @classmethod
    def generate_ai_prompt(cls, results: Dict[str, Any]) -> str:
        """Генерирует промпт для LLM на основе результатов теста"""
        
        style_descriptions = {
            'visual': 'Визуал - лучше воспринимает информацию через изображения, схемы, диаграммы',
            'auditory': 'Аудиал - лучше усваивает через слух, объяснения, обсуждения',
            'readwrite': 'Чтение/Письмо - предпочитает тексты, конспекты, записи',
            'kinesthetic': 'Кинестетик - учится через действие, практику, движение',
            'mixed': 'Смешанный тип - сочетает несколько стилей восприятия'
        }
        
        prompt = f"""На основе результатов когнитивного теста пользователя сгенерируй персонализированные рекомендации по обучению.

ДАННЫЕ ПОЛЬЗОВАТЕЛЯ:
1. Стиль обучения: {results['learning_style']} ({style_descriptions.get(results['learning_style'], '')})
2. Оценка памяти: {results['memory_score']}/10
3. Оценка самодисциплины: {results['discipline_score']}/10
4. Длительность концентрации: {results['concentration_span']} минут
5. Предпочтительное время: {results['preferred_study_time']}

СГЕНЕРИРУЙ РЕКОМЕНДАЦИИ ПО СЛЕДУЮЩЕЙ СТРУКТУРЕ:
1. ФОРМАТ ОБУЧЕНИЯ:
- Основной рекомендуемый формат (видео/аудио/текст/практика)
- Альтернативные форматы
- Частота и длительность учебных сессий

2. СТРАТЕГИЯ ОБУЧЕНИЯ:
- Методы повторения (интервальные повторения, мнемотехники и т.д.)
- Методы конспектирования
- Подход к сложным темам

3. ГЕЙМИФИКАЦИЯ:
- Типы ачивок, которые будут мотивировать пользователя
- Рекомендации по системе XP
- Методы поддержания вовлеченности

4. ПРАКТИЧЕСКИЕ СОВЕТЫ:
- Конкретные инструменты или техники
- Рекомендации по расписанию
- Советы по преодолению прокрастинации

ОТВЕТ ДАЙ В ФОРМАТЕ JSON:
{{
  "format": {{
    "primary": "текст с описанием",
    "alternatives": ["список", "альтернатив"],
    "session_duration": число в минутах,
    "sessions_per_week": число
  }},
  "strategy": {{
    "repetition_methods": ["список", "методов"],
    "note_taking": "текст",
    "difficult_topics": "текст"
  }},
  "gamification": {{
    "achievement_types": ["список", "типов"],
    "xp_recommendations": "текст",
    "engagement_tips": "текст"
  }},
  "practical_tips": {{
    "tools": ["список", "инструментов"],
    "schedule": "текст",
    "procrastination": "текст"
  }}
}}"""
        
        return prompt