# courses/urls.py
from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('add/', views.add_course, name='add_course'),
    path('list/', views.course_list, name='course_list'),
    path('detail/<int:course_id>/', views.course_detail, name='course_detail'),
]