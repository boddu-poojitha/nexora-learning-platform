# quiz_app/admin.py
from django.contrib import admin
from .models import Contestant, QuizResult, UserProfile

admin.site.register(Contestant)
admin.site.register(QuizResult)
admin.site.register(UserProfile)