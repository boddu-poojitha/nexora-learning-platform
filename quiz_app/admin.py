# quiz_app/admin.py
from django.contrib import admin
from .models import Contestant, QuizResult

admin.site.register(Contestant)
admin.site.register(QuizResult)