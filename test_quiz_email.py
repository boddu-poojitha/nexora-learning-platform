import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexora_quiz_project.settings')
django.setup()

from django.test import Client
from django.urls import reverse

def test_quiz_flow():
    client = Client()
    print("1. Starting Quiz Flow...")
    response = client.post(reverse('quiz_app:start_quiz'), {
        'name': 'Test User',
        'email': 'test@example.com',
        'language': 'Python'
    })
    if response.status_code != 302:
        print("Failed to start quiz!")
        return
    print("Quiz started successfully. Redirected to:", response.url)
    
    print("2. Answering 5 questions...")
    for i in range(5):
        # We don't care if the answer is correct for this test
        response = client.post(reverse('quiz_app:quiz'), {'answer': 'test'})
        if response.status_code == 302:
            print(f"Finished at question {i+1}. Redirected to:", response.url)
            break
        elif response.status_code != 200:
            print("Failed at question", i+1)
            return

    print("3. Checking Result Page (This will trigger send_mail)...")
    result_response = client.get(reverse('quiz_app:result'))
    print("Result page status code:", result_response.status_code)
    print("Email sent status in session:", client.session.get('email_sent'))
    
if __name__ == '__main__':
    test_quiz_flow()
