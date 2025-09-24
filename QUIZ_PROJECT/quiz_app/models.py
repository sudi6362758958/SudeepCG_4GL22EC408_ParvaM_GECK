from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# ✅ Custom User model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


# ✅ Quiz model
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration = models.IntegerField(default=10)  # in minutes
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# ✅ Question model
# quiz_app/models.py
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_answers = models.JSONField(default=list)  # stores ["option1", "option3"]
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_correct_answers_list(self):
        return self.correct_answers or []   # ✅ Already a list, just return it
    
    def __str__(self):
        return self.text[:50]
    
# ✅ StudentResult model (stores detailed results)
class StudentResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} - {self.score}/{self.total}"


# ✅ Result model (optional summary/graph use)
class Result(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()  # percentage or marks
    taken_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.quiz} ({self.score})"
