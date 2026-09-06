# quiz_app/views.py
import random
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Avg, Count
from .models import QuizResult, UserProfile

# --- Quiz Questions Data (remains the same) ---
QUIZ_QUESTIONS = {
    'C': [
        {'question': 'What is the entry point of a C program?', 'options': ['start()', 'main()', 'run()', 'begin()'], 'answer': 'main()'},
        {'question': 'Which header file is used for input/output operations in C?', 'options': ['stdio.h', 'stdlib.h', 'math.h', 'string.h'], 'answer': 'stdio.h'},
        {'question': 'What is the size of an int in C (typically)?', 'options': ['1 byte', '2 bytes', '4 bytes', '8 bytes'], 'answer': '4 bytes'},
        {'question': 'Which of the following is a logical operator in C?', 'options': ['+', '*', '&&', '/'], 'answer': '&&'},
        {'question': 'What is a pointer in C?', 'options': ['A variable that stores an integer', 'A variable that stores a memory address', 'A function', 'A data type'], 'answer': 'A variable that stores a memory address'},
        {'question': 'How do you declare a constant in C?', 'options': ['const int x = 10;', '#define X 10', 'both a and b', 'None of the above'], 'answer': 'both a and b'},
        {'question': 'Which function is used to allocate dynamic memory in C?', 'options': ['malloc()', 'calloc()', 'realloc()', 'all of the above'], 'answer': 'all of the above'},
        {'question': 'What is the purpose of the `break` statement?', 'options': ['To exit a loop or switch statement', 'To skip an iteration', 'To continue to the next iteration', 'To define a new function'], 'answer': 'To exit a loop or switch statement'},
        {'question': 'Which of the following is not a data type in C?', 'options': ['int', 'float', 'boolean', 'char'], 'answer': 'boolean'},
        {'question': 'What is the operator for logical NOT?', 'options': ['&', '!', '|', '~'], 'answer': '!'},
        {'question': 'What does `NULL` represent in C?', 'options': ['Zero', 'An empty string', 'A null pointer', 'An error'], 'answer': 'A null pointer'},
        {'question': 'Which loop executes at least once?', 'options': ['for', 'while', 'do-while', 'if'], 'answer': 'do-while'},
        {'question': 'What is the format specifier for printing a float?', 'options': ['%d', '%f', '%c', '%s'], 'answer': '%f'},
        {'question': 'Which of these is a valid identifier?', 'options': ['1name', '_name', 'name-1', 'name 1'], 'answer': '_name'},
        {'question': 'What is the default value of a global variable in C?', 'options': ['Garbage value', '0', 'NULL', 'Undefined'], 'answer': '0'},
        {'question': 'Which keyword is used to return from a function?', 'options': ['exit', 'quit', 'return', 'break'], 'answer': 'return'},
        {'question': 'What is the function of `sizeof` operator?', 'options': ['Calculates memory address', 'Returns size of a variable or type', 'Compares two values', 'Performs bitwise operation'], 'answer': 'Returns size of a variable or type'},
        {'question': 'What is the purpose of `goto` statement?', 'options': ['To jump to a labeled statement', 'To exit the program', 'To call a function', 'To include a header file'], 'answer': 'To jump to a labeled statement'},
        {'question': 'Which operator is used for modulus?', 'options': ['/', '%', '*', '+'], 'answer': '%'},
        {'question': 'How many keywords are there in C?', 'options': ['24', '32', '48', '64'], 'answer': '32'},
    ],
    'Python': [
        {'question': 'Which of the following is mutable in Python?', 'options': ['tuple', 'string', 'list', 'int'], 'answer': 'list'},
        {'question': 'How do you comment a single line in Python?', 'options': ['// comment', '# comment', '/* comment */', '-- comment'], 'answer': '# comment'},
        {'question': 'Which keyword is used to define a function in Python?', 'options': ['func', 'def', 'function', 'define'], 'answer': 'def'},
        {'question': 'What is the output of `type([])`?', 'options': ['<class \'list\'>', '<class \'tuple\'>', '<class \'dict\'>', '<class \'set\'>'], 'answer': '<class \'list\'>'},
        {'question': 'Which method is used to add an item to the end of a list?', 'options': ['insert()', 'append()', 'add()', 'put()'], 'answer': 'append()'},
        {'question': 'What is PEP 8?', 'options': ['A Python error code', 'A style guide for Python code', 'A Python package manager', 'A type of Python loop'], 'answer': 'A style guide for Python code'},
        {'question': 'Which of these is an immutable data type?', 'options': ['list', 'dictionary', 'set', 'string'], 'answer': 'string'},
        {'question': 'What is the purpose of `__init__` method?', 'options': ['To destroy an object', 'To initialize an object\'s attributes', 'To print an object', 'To define a class'], 'answer': 'To initialize an object\'s attributes'},
        {'question': 'How do you open a file in read mode in Python?', 'options': ['open("file.txt", "w")', 'open("file.txt", "r")', 'open("file.txt", "a")', 'open("file.txt", "x")'], 'answer': 'open("file.txt", "r")'},
        {'question': 'What is the output of `2 ** 3`?', 'options': ['6', '8', '9', '5'], 'answer': '8'},
        {'question': 'Which module is used for regular expressions?', 'options': ['os', 'sys', 're', 'math'], 'answer': 're'},
        {'question': 'What is a virtual environment in Python?', 'options': ['A cloud server', 'An isolated Python environment', 'A debugging tool', 'A web framework'], 'answer': 'An isolated Python environment'},
        {'question': 'How do you remove an element from a set?', 'options': ['delete()', 'remove()', 'pop()', 'discard()'], 'answer': 'remove()'},
        {'question': 'What is the purpose of `pass` statement?', 'options': ['To skip a block of code', 'To indicate an empty block', 'To terminate the program', 'To define a variable'], 'answer': 'To indicate an empty block'},
        {'question': 'Which operator is used for string concatenation?', 'options': ['-', '*', '+', '/'], 'answer': '+'},
        {'question': 'What is `pip` in Python?', 'options': ['A standard library', 'A package installer', 'A type of data structure', 'A built-in function'], 'answer': 'A package installer'},
        {'question': 'What is the correct way to import a module named `my_module`?', 'options': ['include my_module', 'import my_module', 'require my_module', 'use my_module'], 'answer': 'import my_module'},
        {'question': 'What is slicing in Python?', 'options': ['Dividing a number', 'Extracting a portion of a sequence', 'Cutting a string', 'Rounding a float'], 'answer': 'Extracting a portion of a sequence'},
        {'question': 'What is the output of `len("hello")`?', 'options': ['4', '5', '6', 'Error'], 'answer': '5'},
        {'question': 'Which of these is used for exception handling?', 'options': ['if/else', 'try/except', 'for/in', 'while/break'], 'answer': 'try/except'},
    ],
    'Java': [
        {'question': 'What is the entry point of a Java application?', 'options': ['start()', 'main()', 'run()', 'begin()'], 'answer': 'main()'},
        {'question': 'Which keyword is used to inherit a class in Java?', 'options': ['implements', 'extends', 'inherits', 'uses'], 'answer': 'extends'},
        {'question': 'Which of the following is not a primitive data type in Java?', 'options': ['int', 'float', 'String', 'boolean'], 'answer': 'String'},
        {'question': 'What is the default value of an instance variable of type `int` in Java?', 'options': ['null', '0', 'undefined', 'garbage value'], 'answer': '0'},
        {'question': 'Which of the following is used to handle exceptions in Java?', 'options': ['try-catch', 'if-else', 'for-loop', 'switch-case'], 'answer': 'try-catch'},
        {'question': 'What is JVM?', 'options': ['Java Virtual Machine', 'Java Vector Model', 'Java Validation Method', 'Java Visual Manager'], 'answer': 'Java Virtual Machine'},
        {'question': 'Which access modifier makes a member accessible only within the same class?', 'options': ['public', 'protected', 'private', 'default'], 'answer': 'private'},
        {'question': 'How do you create an object of a class `MyClass`?', 'options': ['MyClass obj;', 'new MyClass();', 'MyClass obj = new MyClass();', 'create MyClass obj;'], 'answer': 'MyClass obj = new MyClass();'},
        {'question': 'Which interface is used to create a thread?', 'options': ['Runnable', 'Serializable', 'Cloneable', 'Comparable'], 'answer': 'Runnable'},
        {'question': 'What is the superclass of all classes in Java?', 'options': ['Class', 'Object', 'System', 'Main'], 'answer': 'Object'},
        {'question': 'Which keyword is used to prevent method overriding?', 'options': ['static', 'final', 'abstract', 'void'], 'answer': 'final'},
        {'question': 'What is the purpose of `static` keyword?', 'options': ['To make a variable constant', 'To associate a member with the class itself', 'To create a new instance', 'To hide implementation details'], 'answer': 'To associate a member with the class itself'},
        {'question': 'Which package contains the `ArrayList` class?', 'options': ['java.io', 'java.util', 'java.lang', 'java.net'], 'answer': 'java.util'},
        {'question': 'What is the concept of `Polymorphism`?', 'options': ['Ability of an object to take on many forms', 'Encapsulation of data', 'Hiding implementation details', 'Creating multiple threads'], 'answer': 'Ability of an object to take on many forms'},
        {'question': 'Which method is used to compare two strings for equality in Java?', 'options': ['==', 'equals()', 'compare()', 'match()'], 'answer': 'equals()'},
        {'question': 'What is the purpose of `this` keyword?', 'options': ['Refers to the superclass', 'Refers to the current object instance', 'Refers to a static variable', 'Refers to an outer class'], 'answer': 'Refers to the current object instance'},
        {'question': 'Which statement is used to terminate a loop or switch statement?', 'options': ['continue', 'exit', 'break', 'return'], 'answer': 'break'},
        {'question': 'What is the default access modifier for a class in Java?', 'options': ['public', 'private', 'protected', 'default (package-private)'], 'answer': 'default (package-private)'},
        {'question': 'What is an `abstract` class?', 'options': ['A class that cannot be instantiated', 'A class that contains only abstract methods', 'A class with no methods', 'A class that is final'], 'answer': 'A class that cannot be instantiated'},
        {'question': 'Which of these is a checked exception?', 'options': ['NullPointerException', 'ArrayIndexOutOfBoundsException', 'IOException', 'ClassCastException'], 'answer': 'IOException'},
    ]
}


def is_admin_user(user):
    if not user or not user.is_authenticated:
        return False
    if user.is_staff or user.is_superuser:
        return True
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        return False
    return profile.role == 'ADMIN'


def index(request):
    return render(request, 'index.html')


@login_required(login_url=reverse_lazy('quiz_app:login'))
def quiz_start_page(request):
    return render(request, 'quiz_start.html')


def redirect_to_admin_dashboard(request):
    return redirect(reverse('quiz_app:admin_dashboard'))


def redirect_to_quiz_start(request):
    return redirect(reverse('quiz_app:quiz_start'))


def redirect_to_quiz_result(request):
    return redirect(reverse('quiz_app:result'))


@login_required(login_url=reverse_lazy('quiz_app:login'))
def start_quiz(request):
    if request.method == 'POST':
        selected_language = request.POST.get('language')
        if not selected_language:
            return render(request, 'quiz_start.html', {'error_message': 'Please select a programming language.'})

        contestant_name = request.user.get_full_name() or request.user.username
        contestant_email = request.user.email
        request.session['contestant_name'] = contestant_name
        request.session['contestant_email'] = contestant_email
        request.session['selected_language'] = selected_language

        all_questions_for_lang = QUIZ_QUESTIONS.get(selected_language, [])
        if len(all_questions_for_lang) < 5:
            return render(request, 'quiz_start.html', {'error_message': f'Not enough questions available for {selected_language}. Please choose another.'})

        request.session['quiz_questions'] = random.sample(all_questions_for_lang, 5)
        request.session['current_question_index'] = 0
        request.session['score'] = 0

        return redirect(reverse('quiz_app:quiz'))
    return redirect(reverse('quiz_app:quiz_start'))


@login_required(login_url=reverse_lazy('quiz_app:login'))
def quiz(request):
    if 'quiz_questions' not in request.session or 'current_question_index' not in request.session:
        return redirect(reverse('quiz_app:quiz_start'))

    quiz_questions = request.session['quiz_questions']
    current_question_index = request.session['current_question_index']

    if request.method == 'POST':
        user_answer = request.POST.get('answer')
        correct_answer = quiz_questions[current_question_index]['answer']

        if user_answer == correct_answer:
            request.session['score'] += 1

        request.session['current_question_index'] += 1
        current_question_index = request.session['current_question_index']

    if current_question_index < len(quiz_questions):
        question_data = quiz_questions[current_question_index]
        question_number = current_question_index + 1
        total_questions = len(quiz_questions)
        progress_percent = int((question_number / total_questions) * 100) if quiz_questions else 0
        is_final_question = question_number == total_questions
        return render(request, 'quiz.html', {
            'question': question_data['question'],
            'options': question_data['options'],
            'question_number': question_number,
            'total_questions': total_questions,
            'progress_percent': progress_percent,
            'is_final_question': is_final_question
        })
    else:
        contestant_id = request.session.get('contestant_id')
        score = request.session['score']
        total_questions = len(quiz_questions)
        language = request.session['selected_language']

        if request.user.is_authenticated:
            try:
                QuizResult.objects.create(
                    user=request.user,
                    language=language,
                    score=score,
                    total_questions=total_questions
                )
            except Exception as e:
                print(f"Error storing quiz result for user: {e}")
        elif contestant_id:
            try:
                contestant = Contestant.objects.get(id=contestant_id)
                QuizResult.objects.create(
                    contestant=contestant,
                    language=language,
                    score=score,
                    total_questions=total_questions
                )
            except Contestant.DoesNotExist:
                print("Contestant not found for saving quiz result.")
            except Exception as e:
                print(f"Error storing quiz result: {e}")
        else:
            print("Failed to store quiz results due to missing user/contestant ID.")

        email_sent = send_quiz_result_email(
            request.session['contestant_email'],
            request.session['contestant_name'],
            language,
            score,
            total_questions
        )
        request.session['email_sent'] = email_sent

        return redirect(reverse('quiz_app:result'))


def result(request):
    if 'score' not in request.session or 'contestant_name' not in request.session:
        return redirect(reverse('quiz_app:index'))

    score = request.session['score']
    total_questions = len(request.session['quiz_questions'])
    contestant_name = request.session['contestant_name']
    language = request.session['selected_language']
    email_sent = request.session.get('email_sent', False)

    # Clear session data after displaying results
    request.session.pop('quiz_questions', None)
    request.session.pop('current_question_index', None)
    request.session.pop('score', None)
    request.session.pop('contestant_id', None)
    request.session.pop('contestant_name', None)
    request.session.pop('contestant_email', None)
    request.session.pop('selected_language', None)
    request.session.pop('email_sent', None)

    return render(request, 'result.html', {
        'name': contestant_name,
        'score': score,
        'total': total_questions,
        'language': language,
        'email_sent': email_sent
    })


def send_quiz_result_email(to_email, contestant_name, language, score, total_questions):
    subject = f"Your Quiz Results: {language} Programming Language"
    body = f"""
    Dear {contestant_name},

    Thank you for participating in our programming language quiz!

    Here are your results for the {language} quiz:
    Your Score: {score} out of {total_questions}

    Keep practicing and improving your skills!

    Best regards,
    The Nexora Quiz Team
    """
    try:
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [to_email],
            fail_silently=True,
            timeout=5,  # Prevents server hanging on email send
        )
        print(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False

def send_welcome_email(to_email, full_name):
    subject = 'Welcome to Nexora Learning Platform'
    body = f"""
    Hi {full_name},

    Welcome to Nexora! Your account is ready, and you can now start practicing quizzes in C, Python, and Java.

    We look forward to helping you build stronger programming skills.

    Best regards,
    The Nexora Team
    """
    try:
        # Avoid hanging if EMAIL_HOST_USER is missing or empty
        if not getattr(settings, 'EMAIL_HOST_USER', None):
            print("EMAIL_HOST_USER not configured. Skipping welcome email.")
            return False

        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [to_email],
            fail_silently=True,
            timeout=3,  # Forces connection to abort after 3 seconds instead of hanging Gunicorn
        )
        return True
    except Exception as e:
        print(f"Failed to send welcome email to {to_email}: {e}")
        return False    

# --- Authentication and Role Views ---

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([name, email, password, confirm_password]):
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'register.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'register.html')
        
        try:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
            UserProfile.objects.create(user=user, role='LEARNER')
            if send_welcome_email(email, name):
                messages.success(request, 'Account created successfully. Please log in.')
            else:
                messages.warning(request, 'Account created. Please log in. Welcome email could not be delivered right now.')
            return redirect(reverse('quiz_app:login'))
        except Exception as e:
            messages.error(request, 'An error occurred during registration.')
            return render(request, 'register.html')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        login_id = request.POST.get('email')
        password = request.POST.get('password')

        if not all([login_id, password]):
            messages.error(request, 'Please provide both email/username and password.')
            return render(request, 'login.html')

        # Try to authenticate using the provided ID as a username
        user = authenticate(request, username=login_id, password=password)
        
        # If that fails, try treating it as an email address
        if user is None:
            try:
                user_obj = User.objects.get(email=login_id)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
            except User.MultipleObjectsReturned:
                user_obj = User.objects.filter(email=login_id).first()
                user = authenticate(request, username=user_obj.username, password=password)

        if user is not None:
            login(request, user)
            if is_admin_user(user):
                return redirect(reverse('quiz_app:admin_dashboard'))
            return redirect(reverse('quiz_app:dashboard'))
        else:
            messages.error(request, 'Invalid credentials.')
            return render(request, 'login.html')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect(reverse('quiz_app:index'))

@login_required(login_url=reverse_lazy('quiz_app:login'))
def learner_dashboard_view(request):
    if is_admin_user(request.user):
        return redirect(reverse('quiz_app:admin_dashboard'))

    recent_results = QuizResult.objects.filter(user=request.user).order_by('-id')[:5]
    attempt_count = QuizResult.objects.filter(user=request.user).count()
    latest_result = recent_results.first() if recent_results else None
    
    return render(request, 'learner_dashboard.html', {
        'recent_results': recent_results,
        'username': request.user.first_name or request.user.username,
        'attempt_count': attempt_count,
        'latest_result': latest_result
    })

@user_passes_test(is_admin_user, login_url=reverse_lazy('quiz_app:login'), redirect_field_name=None)
def admin_dashboard_view(request):
    learner_count = UserProfile.objects.filter(role='LEARNER').count()
    total_attempts = QuizResult.objects.count()
    average_score = QuizResult.objects.aggregate(avg_score=Avg('score'))['avg_score'] or 0
    recent_results = QuizResult.objects.select_related('user', 'contestant').order_by('-id')[:8]

    recent_activity = []
    for result in recent_results:
        if result.user:
            display_name = result.user.get_full_name() or result.user.username
            display_email = result.user.email
            timestamp = result.user.date_joined
        else:
            display_name = result.contestant.name if result.contestant else 'Anonymous'
            display_email = result.contestant.email if result.contestant else 'N/A'
            timestamp = result.contestant.timestamp if result.contestant else None

        recent_activity.append({
            'name': display_name,
            'email': display_email,
            'language': result.language,
            'score': result.score,
            'total_questions': result.total_questions,
            'timestamp': timestamp,
        })

    learner_summaries = []
    for learner in User.objects.filter(profile__role='LEARNER').select_related('profile').order_by('-date_joined'):
        learner_results = QuizResult.objects.filter(user=learner).order_by('-id')
        latest_result = learner_results.first()
        learner_summaries.append({
            'name': learner.get_full_name() or learner.username,
            'email': learner.email,
            'registered_on': learner.date_joined,
            'attempt_count': learner_results.count(),
            'latest_score': latest_result.score if latest_result else None,
        })

    language_stats = []
    for language in ['C', 'Python', 'Java']:
        language_result = QuizResult.objects.filter(language=language).aggregate(
            attempt_count=Count('id'),
            average_score=Avg('score'),
            average_total_questions=Avg('total_questions'),
        )
        average_score_value = language_result['average_score'] or 0
        average_total_questions = language_result['average_total_questions'] or 1
        score_percentage = round((average_score_value / average_total_questions) * 100, 1) if average_total_questions else 0
        language_stats.append({
            'language': language,
            'attempt_count': language_result['attempt_count'] or 0,
            'average_score': round(average_score_value, 1),
            'score_percentage': score_percentage,
        })

    return render(request, 'admin_dashboard.html', {
        'learner_count': learner_count,
        'total_attempts': total_attempts,
        'average_score': round(average_score, 1),
        'recent_activity': recent_activity,
        'learner_summaries': learner_summaries,
        'language_stats': language_stats,
        'email_delivery_available': hasattr(QuizResult, 'email_sent'),
        'username': request.user.first_name or request.user.username
    })