# courses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.TestAPIView.as_view(), name='test_api'),
    path('api/cognitive-test/questions/', views.CognitiveTestQuestionsView.as_view(), name='cognitive_test_questions'),
    path('api/cognitive-test/submit/', views.SubmitCognitiveTestView.as_view(), name='submit_cognitive_test'),
]