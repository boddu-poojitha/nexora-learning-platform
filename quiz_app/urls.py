# quiz_app/urls.py
from django.urls import path
from . import views

app_name = 'quiz_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('start_quiz/', views.start_quiz, name='start_quiz'),
    path('quiz/', views.quiz, name='quiz'),
    path('result/', views.result, name='result'),
]