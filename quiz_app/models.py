# quiz_app/models.py
from django.db import models

class Contestant(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class QuizResult(models.Model):
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    score = models.IntegerField()
    total_questions = models.IntegerField()

    def __str__(self):
        return f"{self.contestant.name} - {self.language} Quiz"