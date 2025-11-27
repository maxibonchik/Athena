# courses/views.py
import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import CognitiveTest

# Только 3 простых View - ничего лишнего
@method_decorator(csrf_exempt, name='dispatch')
class TestAPIView(View):
    def get(self, request):
        return JsonResponse({
            'message': 'API работает!',
            'status': 'success'
        })

@method_decorator(csrf_exempt, name='dispatch')
class CognitiveTestQuestionsView(View):
    def get(self, request):
        try:
            questions = CognitiveTest.objects.all().order_by('question_number')
            
            questions_data = []
            for question in questions:
                questions_data.append({
                    'id': question.id,
                    'section': question.section,
                    'section_display': question.get_section_display(),
                    'question_number': question.question_number,
                    'question_text': question.question_text,
                    'options': {
                        'a': question.option_a,
                        'b': question.option_b,
                        'c': question.option_c,
                        'd': question.option_d
                    }
                })
            
            return JsonResponse({
                'success': True,
                'questions': questions_data,
                'total_questions': len(questions_data)
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Ошибка загрузки вопросов: {str(e)}'
            }, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class SubmitCognitiveTestView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            answers = data.get('answers', {})
            
            print("📝 Получены ответы:", answers)
            
            # Простой расчет результатов
            def calculate_learning_style(ans):
                styles = {'visual': 0, 'auditory': 0, 'reading': 0, 'kinesthetic': 0}
                for q in range(1, 7):
                    answer = ans.get(str(q))
                    if answer == 'a': styles['visual'] += 1
                    elif answer == 'b': styles['auditory'] += 1
                    elif answer == 'c': styles['reading'] += 1
                    elif answer == 'd': styles['kinesthetic'] += 1
                return max(styles, key=styles.get)
            
            def calculate_score(ans, start, end):
                scores = {'a': 10, 'b': 7, 'c': 4, 'd': 1}
                total = count = 0
                for q in range(start, end + 1):
                    answer = ans.get(str(q))
                    if answer in scores:
                        total += scores[answer]
                        count += 1
                return round(total / count) if count > 0 else 5
            
            results = {
                'learning_style': calculate_learning_style(answers),
                'memory_score': calculate_score(answers, 7, 12),
                'discipline_score': calculate_score(answers, 13, 18)
            }
            
            print("✅ Результаты:", results)
            
            return JsonResponse({
                'success': True,
                'message': 'Тест успешно пройден!',
                'results': results,
                'recommendations': {
                    'learning_format': ['видеоуроки', 'практические задания'],
                    'study_strategy': ['регулярные занятия', 'повторение материала'],
                    'memory_techniques': ['интервальные повторения'],
                    'pace': 'умеренный'
                }
            })
            
        except Exception as e:
            print("❌ Ошибка:", str(e))
            return JsonResponse({
                'success': False,
                'error': f'Ошибка сервера: {str(e)}'
            }, status=500)