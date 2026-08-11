# quiz_app/models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('LEARNER', 'Learner'),
        ('ADMIN', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='LEARNER')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Contestant(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class QuizResult(models.Model):
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    language = models.CharField(max_length=50)
    score = models.IntegerField()
    total_questions = models.IntegerField()

    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.language} Quiz"
        elif self.contestant:
            return f"{self.contestant.name} - {self.language} Quiz"
        return f"Anonymous - {self.language} Quiz"