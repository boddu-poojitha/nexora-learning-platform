import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexora_quiz_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'poojitha'
email = 'poojithab30@example.com'
password = 'NexoraQuiz2026SecurePass#'

user, created = User.objects.get_or_create(username=username, defaults={'email': email})
user.set_password(password)
user.is_staff = True
user.is_superuser = True
user.save()

if created:
    print("Created new superuser 'poojitha' on AWS RDS.")
else:
    print("Updated password for existing superuser 'poojitha' on AWS RDS.")