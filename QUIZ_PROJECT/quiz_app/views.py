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

from .models import Quiz, StudentResult



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


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # set email (form already validated)
            user.email = form.cleaned_data.get('email')
            # If your User model has a 'role' field (custom user model), set it here safely:
            try:
                user.role = form.cleaned_data.get('role')
            except Exception:
                # if your User model doesn't have role, you may save role in a Profile model here
                pass
            user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')  # ensure 'login' url name exists
        # if not valid, fall through to re-render with errors
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

from .models import Result

@login_required
def student_dashboard(request):
    user = request.user

    # Fetch all results for the logged-in student, ordered by latest first
    results = StudentResult.objects.filter(student=user).order_by('-submitted_at')

    # Prepare chart data: only show recent quizzes (limit 5 for example)
    recent_results = results[:5][::-1]  # Reverse to show oldest first in chart

    quiz_labels = [res.quiz.title for res in recent_results]
    quiz_scores = [res.score for res in recent_results]

    context = {
        'user': user,
        'results': results,
        'quiz_labels': quiz_labels,
        'quiz_scores': quiz_scores,
    }

    return render(request, 'quiz_app/student_dashboard.html', context)
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
            quiz.is_active = False  # default draft
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
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz

            # ✅ collect selected correct answers
            selected_answers = request.POST.getlist("correct_answers")
            question.correct_answers = selected_answers

            question.save()
            return redirect("add_question", quiz_id=quiz.id)
    else:
        form = QuestionForm()

    return render(request, "quiz_app/add_question.html", {
        "quiz": quiz,
        "form": form,
        "questions": questions,
        "show_questions_block": True,
    })



@login_required
def delete_question(request, quiz_id, pk):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    question = get_object_or_404(Question, id=pk, quiz=quiz)
    question.delete()
    return redirect('add_question', quiz_id=quiz.id)

@login_required
@never_cache
def edit_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    question = get_object_or_404(Question, id=question_id, quiz=quiz)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)

            # ✅ Get selected checkboxes
            selected = request.POST.getlist("correct_answers")
            question.correct_answers = selected

            question.save()
            return redirect('add_question', quiz_id=quiz.id)
    else:
        form = QuestionForm(instance=question)

    option_fields = [form[f"option{i}"] for i in range(1, 5)]

    return render(request, 'quiz_app/edit_question.html', {
        'quiz': quiz,
        'form': form,
        'question': question,
        'option_fields': option_fields,
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
        "questions": questions,
        "show_questions_block": False,
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
    # guard: only students should attempt (adjust if your role field name differs)
    if getattr(user, 'role', None) != 'student':
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
            # POST names are the question id strings; values are option keys like "option1"
            selected_keys = request.POST.getlist(str(q.id))  # e.g. ["option1", "option3"]
            # Normalize: ensure list of strings
            selected_keys = [s for s in selected_keys if s]

            # Get correct keys from model (your model stores JSON list)
            correct_keys = q.get_correct_answers_list() or []

            # Compare sets for exact-match (all-and-only-correct)
            is_correct = set(selected_keys) == set(correct_keys)

            if is_correct:
                score += 1

            # Convert keys to readable text for the result view
            def key_to_text(key):
                return getattr(q, key) if hasattr(q, key) else key

            selected_texts = [key_to_text(k) for k in selected_keys]
            correct_texts = [key_to_text(k) for k in correct_keys]

            results.append({
                'question': q.text,
                'selected_keys': selected_keys,
                'selected_texts': selected_texts,
                'correct_keys': correct_keys,
                'correct_texts': correct_texts,
                'is_correct': is_correct,
            })

        # Save result (adjust fields if your StudentResult model differs)
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

    # GET request — render attempt page
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

    # Add wrong_answers, percentage, and color for template
    for r in results:
        r.wrong_answers = r.total - r.score
        r.percentage = round((r.score / r.total) * 100, 1)
        if r.percentage >= 75:
            r.color = '#1cc88a'  # green
        elif r.percentage >= 50:
            r.color = '#f6c23e'  # yellow
        else:
            r.color = '#e74a3b'  # red

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
################### Admin Analytics Dashboard #####################

from django.shortcuts import render
from django.db.models import Count, Avg, Max, Min
from .models import Quiz, StudentResult, User   # custom User model

def analytics_dashboard(request):
    # Totals
    total_quizzes = Quiz.objects.count()
    total_students = User.objects.filter(role="student").count()   # only students
    total_attempts = StudentResult.objects.count()

    # Scores
    average_score = StudentResult.objects.aggregate(avg=Avg('score'))['avg'] or 0
    top_score = StudentResult.objects.aggregate(max=Max('score'))['max'] or 0
    low_score = StudentResult.objects.aggregate(min=Min('score'))['min'] or 0

    # Most attempted quiz
    most_attempted_quiz = (
        StudentResult.objects
        .values('quiz__title')
        .annotate(count=Count('id'))
        .order_by('-count')
        .first()
    )

    # Bar chart: Attempts per quiz
    quiz_attempts = (
        StudentResult.objects
        .values('quiz__title')
        .annotate(count=Count('id'))
        .order_by('quiz__title')
    )
    chart_labels = [item['quiz__title'] for item in quiz_attempts]
    chart_data = [item['count'] for item in quiz_attempts]

    # Line chart: student scores
    student_scores = (
        StudentResult.objects
        .select_related('student')
        .values('student__username', 'score')
        .order_by('student__username')
    )
    student_names = [item['student__username'] for item in student_scores]  # ✅ corrected
    scores = [item['score'] for item in student_scores]

    context = {
        'total_quizzes': total_quizzes,
        'total_students': total_students,
        'total_attempts': total_attempts,
        'average_score': average_score,
        'top_score': top_score,
        'low_score': low_score,
        'most_attempted_quiz': most_attempted_quiz,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'student_names': student_names,   # ✅ send correct variable
        'scores': scores,
    }

    return render(request, 'quiz_app/analytics_dashboard.html', context)


# ---------------------------------------------------------------


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Result

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()

    if request.method == "POST":
        score = 0
        total = questions.count()

        for question in questions:
            selected = request.POST.get(str(question.id))  # user’s selected option
            if selected and selected == question.correct_answer:
                score += 1

        percentage = (score / total) * 100 if total > 0 else 0

        # ✅ Save result for the logged-in student
        Result.objects.create(
            student=request.user,
            quiz=quiz,
            score=percentage
        )

        return redirect("student_dashboard")  # change if your URL name is different

    return render(request, "quiz_app/take_quiz.html", {"quiz": quiz, "questions": questions})


######################################################


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import StudentResult

@login_required
def student_dashboard(request):
    results = StudentResult.objects.filter(student=request.user).order_by("submitted_at")

    quiz_labels = [result.quiz.title for result in results]
    quiz_scores = [result.score for result in results]

    # ✅ Ensure they are JSON-safe lists
    from django.utils.safestring import mark_safe
    import json

    context = {
        "results": results,
        "quiz_labels": mark_safe(json.dumps(quiz_labels)),
        "quiz_scores": mark_safe(json.dumps(quiz_scores)),
    }
    return render(request, "quiz_app/student_dashboard.html", context)

########################################################################33

from .models import Quiz

def admin_dashboard(request):
    quizzes = Quiz.objects.all()
    return render(request, "quiz_app/admin_dashboard.html", {"quizzes": quizzes})

# Toggle Publish/Unpublish
def toggle_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == "POST":
        quiz.is_active = not quiz.is_active
        quiz.save()
    return redirect('admin_dashboard')

def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == "POST":
        new_title = request.POST.get("title", "").strip()

        # Basic validation: non-empty title
        if not new_title:
            messages.error(request, "⚠ Quiz title cannot be empty.")
            # Re-render template and preserve the attempted title so user doesn't lose typed text
            return render(request, "quiz_app/edit_quiz.html", {
                "quiz": quiz,
                "attempted_title": request.POST.get("title", "")
            })

        # Save update
        quiz.title = new_title
        quiz.save()
        messages.success(request, "✅ Quiz title updated successfully.")
        return redirect("admin_dashboard")
    # GET
    return render(request, "quiz_app/edit_quiz.html", {"quiz": quiz})
################33

def edit_quiz_time(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == "POST":
        duration = request.POST.get("duration")  # get from form input name="duration"

        if duration and duration.isdigit():
            quiz.duration = int(duration)
            quiz.save()
            messages.success(request, "⏳ Quiz duration updated successfully!")
            return redirect("dashboard")  # or wherever you want to go after saving
        else:
            messages.error(request, "❌ Please enter a valid duration (in minutes).")

    return render(request, "quiz_app/edit_quiz_time.html", {"quiz": quiz})