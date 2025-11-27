# ai/test_scoring.py
import json
from django.utils import timezone

class CognitiveTestScorer:
    """
    Сервис для расчета результатов когнитивного теста
    """
    
    # Маппинг ответов на стили обучения для вопросов 1-6
    LEARNING_STYLE_MAP = {
        1: {'a': 'visual', 'b': 'auditory', 'c': 'reading', 'd': 'kinesthetic'},
        2: {'a': 'visual', 'b': 'auditory', 'c': 'reading', 'd': 'kinesthetic'},
        3: {'a': 'visual', 'b': 'auditory', 'c': 'reading', 'd': 'kinesthetic'},
        4: {'a': 'visual', 'b': 'auditory', 'c': 'reading', 'd': 'kinesthetic'},
        5: {'a': 'visual', 'b': 'auditory', 'c': 'reading', 'd': 'kinesthetic'},
        6: {'a': 'visual', 'b': 'auditory', 'c': 'reading', 'd': 'kinesthetic'},
    }
    
    # Баллы для вопросов памяти (7-12)
    MEMORY_SCORES = {'a': 10, 'b': 7, 'c': 4, 'd': 1}
    
    # Баллы для вопросов самодисциплины (13-18)
    DISCIPLINE_SCORES = {'a': 10, 'b': 7, 'c': 4, 'd': 1}
    
    @classmethod
    def calculate_learning_style(cls, answers):
        """
        Рассчитывает основной стиль обучения на основе ответов на вопросы 1-6
        """
        style_counts = {
            'visual': 0,
            'auditory': 0, 
            'reading': 0,
            'kinesthetic': 0
        }
        
        for q_num in range(1, 7):
            answer = answers.get(str(q_num))
            if answer and q_num in cls.LEARNING_STYLE_MAP:
                style = cls.LEARNING_STYLE_MAP[q_num][answer]
                style_counts[style] += 1
        
        # Находим стиль с максимальным количеством ответов
        max_style = max(style_counts, key=style_counts.get)
        max_count = style_counts[max_style]
        
        # Проверяем, нет ли близких конкурентов (разница менее 2)
        close_competitors = [
            style for style, count in style_counts.items()
            if style != max_style and max_count - count < 2
        ]
        
        if close_competitors:
            return 'mixed'
        return max_style
    
    @classmethod
    def calculate_memory_score(cls, answers):
        """
        Рассчитывает оценку памяти (1-10) на основе вопросов 7-12
        """
        total_score = 0
        question_count = 0
        
        for q_num in range(7, 13):
            answer = answers.get(str(q_num))
            if answer and answer in cls.MEMORY_SCORES:
                total_score += cls.MEMORY_SCORES[answer]
                question_count += 1
        
        if question_count == 0:
            return 5  # Среднее значение по умолчанию
            
        average_score = total_score / question_count
        return round(average_score)
    
    @classmethod
    def calculate_discipline_score(cls, answers):
        """
        Рассчитывает оценку самодисциплины (1-10) на основе вопросов 13-18
        """
        total_score = 0
        question_count = 0
        
        for q_num in range(13, 19):
            answer = answers.get(str(q_num))
            if answer and answer in cls.DISCIPLINE_SCORES:
                total_score += cls.DISCIPLINE_SCORES[answer]
                question_count += 1
        
        if question_count == 0:
            return 5  # Среднее значение по умолчанию
            
        average_score = total_score / question_count
        return round(average_score)
    
    @classmethod
    def process_test_results(cls, user_answers):
        """
        Основной метод для обработки результатов теста
        """
        learning_style = cls.calculate_learning_style(user_answers)
        memory_score = cls.calculate_memory_score(user_answers)
        discipline_score = cls.calculate_discipline_score(user_answers)
        
        # Детальная аналитика для отображения пользователю
        detailed_scores = {
            'learning_style_breakdown': {
                'visual': 0, 'auditory': 0, 'reading': 0, 'kinesthetic': 0
            },
            'memory_breakdown': {},
            'discipline_breakdown': {}
        }
        
        # Подсчет стилей обучения
        for q_num in range(1, 7):
            answer = user_answers.get(str(q_num))
            if answer and q_num in cls.LEARNING_STYLE_MAP:
                style = cls.LEARNING_STYLE_MAP[q_num][answer]
                detailed_scores['learning_style_breakdown'][style] += 1
        
        # Подсчет баллов памяти
        memory_details = {}
        for q_num in range(7, 13):
            answer = user_answers.get(str(q_num))
            if answer:
                memory_details[f'question_{q_num}'] = {
                    'answer': answer,
                    'score': cls.MEMORY_SCORES.get(answer, 0)
                }
        detailed_scores['memory_breakdown'] = memory_details
        
        # Подсчет баллов самодисциплины
        discipline_details = {}
        for q_num in range(13, 19):
            answer = user_answers.get(str(q_num))
            if answer:
                discipline_details[f'question_{q_num}'] = {
                    'answer': answer,
                    'score': cls.DISCIPLINE_SCORES.get(answer, 0)
                }
        detailed_scores['discipline_breakdown'] = discipline_details
        
        return {
            'learning_style': learning_style,
            'memory_score': memory_score,
            'discipline_score': discipline_score,
            'detailed_scores': detailed_scores,
            'calculated_at': timezone.now().isoformat()
        }