# quiz_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Quiz, Question
from django.contrib.auth import get_user_model


# ------------------------
# User Registration Form
# ------------------------
User = get_user_model()   # ✅ use your custom User model
ROLE_CHOICES = (
    ('student', 'Student'),
    ('admin', 'Admin'),
)

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'id_email',
            'placeholder': 'you@example.com'
        })
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_role'
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "role")
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_username',
                'placeholder': 'Username'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'id': 'id_password1',
                'placeholder': 'Password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'id': 'id_password2',
                'placeholder': 'Confirm Password'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email


# ------------------------
# Login Form
# ------------------------
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'form-control'})
    )


# ------------------------
# Quiz Form
# ------------------------
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter quiz title"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter quiz description",
                "rows": 3
            }),
        }


# ------------------------
# Question Form
# ------------------------
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text", "option1", "option2", "option3", "option4"]