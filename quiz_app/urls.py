# quiz_app/urls.py
from django.urls import path
from . import views

app_name = 'quiz_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.learner_dashboard_view, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('quiz/start/', views.quiz_start_page, name='quiz_start'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz/result/', views.result, name='result'),
    path('start_quiz/', views.start_quiz, name='start_quiz'),
    path('result/', views.redirect_to_quiz_result, name='legacy_result'),
]