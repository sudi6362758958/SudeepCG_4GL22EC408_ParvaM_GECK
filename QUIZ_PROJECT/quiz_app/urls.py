from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/quiz/create/', views.create_quiz, name='create_quiz'),
    path("quiz/<int:quiz_id>/delete/", views.delete_quiz, name="delete_quiz"),
    path('admin/quiz/<int:quiz_id>/view/', views.view_questions, name="view_questions"),
    path('admin/quiz/<int:quiz_id>/add-question/', views.add_question, name='add_question'),
    path('admin/quiz/<int:quiz_id>/edit-question/<int:pk>/', views.edit_question, name='edit_question'),
    path('admin/quiz/<int:quiz_id>/delete-question/<int:pk>/', views.delete_question, name='delete_question'),
    path('admin/quiz/<int:quiz_id>/questions/', views.view_questions, name="view_questions"),
    path('student/quizzes/', views.student_quiz_list, name='student_quiz_list'),
    path('quiz/<int:quiz_id>/attempt/', views.attempt_quiz, name='attempt_quiz'),
    path('student/results/', views.student_results, name='student_results'),
    path('admin/view-results/', views.view_all_results, name='view_all_results'),
    path('quiz/<int:quiz_id>/leaderboard/', views.leaderboard, name='leaderboard'),
    path('admin/analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/quiz/<int:quiz_id>/view/', views.view_questions, name='view_questions'),
    path('admin/quiz/<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),
]