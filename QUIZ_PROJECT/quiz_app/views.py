# quiz_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Max, Min
from .forms import UserRegistrationForm, UserLoginForm, QuizForm, QuestionForm
from .models import User, Quiz, StudentResult
from .models import Question
from django.urls import reverse
from django.contrib import messages


# ------------------- Authentication -------------------

def home(request):
    return render(request, 'quiz_app/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'quiz_app/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'quiz_app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ------------------- Dashboards -------------------

@login_required
@never_cache 
def dashboard(request):
    user = request.user
    if user.role == 'admin':
        quizzes = Quiz.objects.filter(created_by=user)
        return render(request, 'quiz_app/admin_dashboard.html', {
            'user': user,
            'quizzes': quizzes
        })
    else:
        return render(request, 'quiz_app/student_dashboard.html', {
            'user': user
        })


# ------------------- Quiz Management -------------------

@login_required
def create_quiz(request):
    user = request.user
    if user.role != 'admin':
        return redirect('dashboard')

    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = user
            quiz.save()
            return redirect('dashboard')
    else:
        form = QuizForm()

    return render(request, 'quiz_app/create_quiz.html', {'form': form, 'user': user})
    

@login_required
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == "POST":
        quiz.delete()
        messages.success(request, "Quiz deleted successfully!")
        return redirect("dashboard")

    # On GET → show confirmation page
    return render(request, "quiz_app/delete_quiz.html", {"quiz": quiz})



@login_required
@never_cache
def add_question(request, quiz_id):
    # Get the quiz object
    quiz = get_object_or_404(Quiz, id=quiz_id)
    # Get all questions for this quiz
    questions = Question.objects.filter(quiz=quiz)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # Create question object but don't save yet
            question = form.save(commit=False)
            # Map selected correct_answer ('option1', etc.) to actual text
            selected_option = question.correct_answer  # 'option1', 'option2', etc.
            question.correct_answer = getattr(question, selected_option)  # Store actual text
            question.quiz = quiz  # Associate with the quiz
            question.save()  # Save to DB
            return redirect('add_question', quiz_id=quiz.id)
    else:
        form = QuestionForm()

    return render(request, 'quiz_app/add_question.html', {
        'quiz': quiz,
        'questions': questions,
        'form': form
    })


@login_required
def delete_question(request, quiz_id, pk):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    question = get_object_or_404(Question, id=pk, quiz=quiz)
    question.delete()
    return redirect('add_question', quiz_id=quiz.id)

@login_required
@never_cache
def edit_question(request, quiz_id, pk):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    question = get_object_or_404(Question, id=pk, quiz=quiz)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            # Save actual option text for correct_answer
            selected_option = form.cleaned_data['correct_answer']
            question = form.save(commit=False)
            question.correct_answer = getattr(question, selected_option)
            question.save()
            return redirect('add_question', quiz_id=quiz.id)
    else:
        # Pre-select the correct option key in dropdown
        # Find which option matches correct_answer
        for opt in ['option1', 'option2', 'option3', 'option4']:
            if getattr(question, opt) == question.correct_answer:
                question.correct_answer = opt
                break

        form = QuestionForm(instance=question)

    return render(request, 'quiz_app/add_question.html', {
        'quiz': quiz,
        'questions': Question.objects.filter(quiz=quiz),
        'form': form,
        'editing': True,
        'question': question
    })




@login_required
@never_cache
def view_questions(request, quiz_id):
    # Get the quiz
    quiz = get_object_or_404(Quiz, id=quiz_id)
    # Get all questions for this quiz
    questions = Question.objects.filter(quiz=quiz)

    return render(request, "quiz_app/add_question.html", {
        "quiz": quiz,
        "questions": questions
    })



# ------------------- Student Quiz Flow -------------------

@login_required
def student_quiz_list(request):
    user = request.user
    if user.role != 'student':
        return redirect('dashboard')

    quizzes = Quiz.objects.filter(is_active=True)

    return render(request, 'quiz_app/student_quiz_list.html', {
        'quizzes': quizzes,
        'user': user,
    })


@login_required
def attempt_quiz(request, quiz_id):
    user = request.user
    if user.role != 'student':
        return redirect('dashboard')

    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    # Prevent reattempt
    if StudentResult.objects.filter(student=user, quiz=quiz).exists():
        return render(request, 'quiz_app/already_attempted.html', {'quiz': quiz})

    if request.method == 'POST':
        score = 0
        total = questions.count()
        results = []

        for q in questions:
            selected = request.POST.get(str(q.id))
            is_correct = selected == q.correct_answer
            if is_correct:
                score += 1
            results.append({
                'question': q.text,
                'selected': selected,
                'correct': q.correct_answer,
                'is_correct': is_correct
            })

        StudentResult.objects.create(
            student=user,
            quiz=quiz,
            score=score,
            total=total
        )

        return render(request, 'quiz_app/quiz_result.html', {
            'quiz': quiz,
            'score': score,
            'total': total,
            'results': results
        })

    return render(request, 'quiz_app/attempt_quiz.html', {
        'quiz': quiz,
        'questions': questions
    })


@login_required
def student_results(request):
    user = request.user
    if user.role != 'student':
        return redirect('dashboard')

    results = StudentResult.objects.filter(student=user)

    return render(request, 'quiz_app/student_results.html', {
        'results': results
    })


# ------------------- Admin Results -------------------

@login_required
def view_all_results(request):
    user = request.user
    if user.role != 'admin':
        return redirect('dashboard')

    quizzes = Quiz.objects.filter(created_by=user)
    selected_quiz_id = request.GET.get('quiz')
    selected_quiz = None
    results = []

    if selected_quiz_id:
        selected_quiz = get_object_or_404(Quiz, id=selected_quiz_id)
        results = StudentResult.objects.filter(quiz=selected_quiz)

    return render(request, 'quiz_app/view_all_results.html', {
        'quizzes': quizzes,
        'results': results,
        'selected_quiz': selected_quiz,
    })


@login_required
def leaderboard(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    all_results = StudentResult.objects.filter(quiz=quiz).order_by('-score', 'submitted_at')

    # Only keep latest per student
    seen_students = set()
    latest_results = []

    for result in all_results:
        if result.student_id not in seen_students:
            latest_results.append(result)
            seen_students.add(result.student_id)

    top_scores = sorted(latest_results, key=lambda r: (-r.score, r.submitted_at))[:5]

    return render(request, 'quiz_app/leaderboard.html', {
        'quiz': quiz,
        'top_scores': top_scores
    })


@login_required
def analytics_dashboard(request):
    user = request.user
    if user.role != 'admin':
        return redirect('dashboard')

    total_quizzes = Quiz.objects.filter(created_by=user).count()
    total_students = User.objects.filter(role='student').count()
    total_attempts = StudentResult.objects.filter(quiz__created_by=user).count()

    average_score = StudentResult.objects.filter(quiz__created_by=user).aggregate(avg_score=Avg('score'))['avg_score']
    top_score = StudentResult.objects.filter(quiz__created_by=user).aggregate(top=Max('score'))['top']
    low_score = StudentResult.objects.filter(quiz__created_by=user).aggregate(low=Min('score'))['low']

    most_attempted_quiz = (
        StudentResult.objects.filter(quiz__created_by=user)
        .values('quiz__title')
        .annotate(count=Count('id'))
        .order_by('-count')
        .first()
    )

    return render(request, 'quiz_app/analytics_dashboard.html', {
        'total_quizzes': total_quizzes,
        'total_students': total_students,
        'total_attempts': total_attempts,
        'average_score': average_score,
        'top_score': top_score,
        'low_score': low_score,
        'most_attempted_quiz': most_attempted_quiz,
    })
